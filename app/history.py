from abc import ABC, abstractmethod
from pathlib import Path
import logging

import pandas as pd

from app.calculation import Calculation


class HistoryObserver(ABC):
    """Abstract base class for calculator observers."""

    @abstractmethod
    def update(
        self,
        event: str,
        calculation: Calculation | None,
        history: list[Calculation],
    ) -> None:
        """Respond to a calculator event."""
        pass

class LoggingObserver(HistoryObserver):
    """Log new calculations to a file."""

    def __init__(self, log_file: str | Path):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(
            f"calculator.history.{id(self)}"
        )
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        handler = logging.FileHandler(
            self.log_file,
            encoding="utf-8",
        )

        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )

        self.logger.addHandler(handler)
        self._handler = handler

    def update(
        self,
        event: str,
        calculation: Calculation | None,
        history: list[Calculation],
    ) -> None:
        if event != "calculation" or calculation is None:
            return

        self.logger.info(
            "%s: %s, %s = %s",
            calculation.operation,
            calculation.operand1,
            calculation.operand2,
            calculation.result,
        )

    def close(self) -> None:
        """Close the file handler when logging is no longer needed."""

        self.logger.removeHandler(self._handler)
        self._handler.close()

class AutoSaveObserver(HistoryObserver):
    """Save history whenever its state changes."""

    def __init__(
        self,
        history_file: str | Path,
        enabled: bool = True,
        encoding: str = "utf-8",
    ):
        self.history_file = Path(history_file)
        self.enabled = enabled
        self.encoding = encoding

    def update(
        self,
        event: str,
        calculation: Calculation | None,
        history: list[Calculation],
    ) -> None:
        if not self.enabled:
            return

        supported_events = {
            "calculation",
            "undo",
            "redo",
            "clear",
            "load",
        }

        if event not in supported_events:
            return

        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        records = [calc.to_dict() for calc in history]

        dataframe = pd.DataFrame(records, columns=columns)

        dataframe.to_csv(
            self.history_file,
            index=False,
            encoding=self.encoding,
        )