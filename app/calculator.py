from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import (
    HistoryObserver,
    LoggingObserver,
    AutoSaveObserver,
)


class Calculator:
    """Manage calculations, history, observers and persistence."""

    COLUMNS = [
        "operation",
        "operand1",
        "operand2",
        "result",
        "timestamp",
    ]

    def __init__(
        self,
        max_history_size: int = 100,
        config: CalculatorConfig | None = None,
    ):
        if config is not None:
            max_history_size = config.max_history_size

        if (
            isinstance(max_history_size, bool)
            or not isinstance(max_history_size, int)
            or max_history_size <= 0
        ):
            raise ValidationError(
                "Maximum history size must be a positive integer."
            )

        self.config = config
        self._max_history_size = max_history_size

        self._history: list[Calculation] = []
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []
        self._observers: list[HistoryObserver] = []

        self._logging_observer = None

        if self.config is not None:
            self._logging_observer = LoggingObserver(
                self.config.log_path
            )
            self.register_observer(self._logging_observer)

            self.register_observer(
                AutoSaveObserver(
                    self.config.history_path,
                    enabled=self.config.auto_save,
                    encoding=self.config.default_encoding,
                )
            )

    def register_observer(self, observer: HistoryObserver) -> None:
        if not isinstance(observer, HistoryObserver):
            raise TypeError(
                "Observer must inherit from HistoryObserver."
            )

        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: HistoryObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(
        self,
        event: str,
        calculation: Calculation | None = None,
    ) -> None:
        for observer in self._observers.copy():
            observer.update(
                event,
                calculation,
                self.get_history(),
            )

    def _create_memento(self) -> CalculatorMemento:
        return CalculatorMemento.create(self._history)

    def _restore_memento(
        self,
        memento: CalculatorMemento,
    ) -> None:
        self._history = memento.restore()

    def _apply_precision(self, result: Decimal) -> Decimal:
        """Round a result to the configured decimal places."""

        if self.config is None:
            return result

        quantizer = Decimal("1").scaleb(
            -self.config.precision
        )

        try:
            with localcontext() as context:
                context.prec = max(
                    28,
                    len(result.as_tuple().digits)
                    + self.config.precision + 2,
                )
                return result.quantize(quantizer)
        except InvalidOperation as error:
            raise OperationError(
                "Cannot apply the configured precision."
            ) from error

    def perform_operation(
        self,
        operation: str,
        operand1,
        operand2,
    ) -> Decimal:
        """Perform a calculation and notify observers."""

        max_value = (
            self.config.max_input_value
            if self.config is not None
            else Decimal("1000000")
        )

        calculation = Calculation.create(
            operation,
            operand1,
            operand2,
            max_value=max_value,
        )

        calculation.result = self._apply_precision(
            calculation.result
        )

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()

        self._history.append(calculation)

        if len(self._history) > self._max_history_size:
            self._history.pop(0)

        self.notify_observers(
            "calculation",
            calculation,
        )

        return calculation.result

    def undo(self) -> bool:
        if not self._undo_stack:
            return False

        self._redo_stack.append(self._create_memento())

        previous_state = self._undo_stack.pop()
        self._restore_memento(previous_state)

        self.notify_observers("undo")
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False

        self._undo_stack.append(self._create_memento())

        next_state = self._redo_stack.pop()
        self._restore_memento(next_state)

        self.notify_observers("redo")
        return True

    def get_history(self) -> list[Calculation]:
        return self._history.copy()

    def get_history_count(self) -> int:
        return len(self._history)

    def clear_history(self) -> None:
        if not self._history:
            return

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()
        self._history.clear()

        self.notify_observers("clear")

    def _history_file(self, file_path=None) -> Path:
        """Resolve the CSV path."""

        if file_path is not None:
            return Path(file_path)

        if self.config is not None:
            return self.config.history_path

        return Path("history/calculator_history.csv")

    def save_history(self, file_path=None) -> Path:
        """Save current history to CSV using pandas."""

        path = self._history_file(file_path)
        encoding = (
            self.config.default_encoding
            if self.config is not None
            else "utf-8"
        )

        path.parent.mkdir(parents=True, exist_ok=True)

        records = [
            calculation.to_dict()
            for calculation in self._history
        ]

        dataframe = pd.DataFrame(
            records,
            columns=self.COLUMNS,
        )

        try:
            dataframe.to_csv(
                path,
                index=False,
                encoding=encoding,
            )
        except (OSError, UnicodeError, ValueError) as error:
            raise OperationError(
                f"Failed to save history: {error}"
            ) from error

        return path

    def load_history(self, file_path=None) -> int:
        """Load calculation history from CSV."""

        path = self._history_file(file_path)
        encoding = (
            self.config.default_encoding
            if self.config is not None
            else "utf-8"
        )

        try:
            dataframe = pd.read_csv(
                path,
                dtype=str,
                keep_default_na=False,
                encoding=encoding,
            )
        except (
            OSError,
            UnicodeError,
            ValueError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as error:
            raise OperationError(
                f"Failed to load history: {error}"
            ) from error

        if list(dataframe.columns) != self.COLUMNS:
            raise OperationError(
                "Invalid CSV columns for calculation history."
            )

        loaded_history = []

        for record in dataframe.to_dict(orient="records"):
            try:
                calculation = Calculation.from_dict(record)

                if (
                    not calculation.operand1.is_finite()
                    or not calculation.operand2.is_finite()
                    or not calculation.result.is_finite()
                ):
                    raise ValueError("Non-finite value in history.")

                loaded_history.append(calculation)

            except (OperationError, ValueError) as error:
                raise OperationError(
                    f"Invalid calculation record: {error}"
                ) from error

        loaded_history = loaded_history[
            -self._max_history_size:
        ]

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()
        self._history = loaded_history

        self.notify_observers("load")

        return len(self._history)

    def close(self) -> None:
        """Release the calculator's own logging handler."""

        if self._logging_observer is not None:
            self.remove_observer(self._logging_observer)
            self._logging_observer.close()
            self._logging_observer = None