from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import ValidationError


class Calculator:
    """Manage calculations, history, undo, and redo."""

    def __init__(self, max_history_size: int = 100):

        if (
            isinstance(max_history_size, bool)
            or not isinstance(max_history_size, int)
            or max_history_size <= 0
        ):
            raise ValidationError(
                "Maximum history size must be a positive integer."
            )

        self._history: list[Calculation] = []
        self._max_history_size = max_history_size

        # Memento stacks
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []

    def _create_memento(self) -> CalculatorMemento:
        """Save the current calculator history state."""

        return CalculatorMemento.create(self._history)

    def _restore_memento(self, memento: CalculatorMemento) -> None:
        """Restore calculator history from a snapshot."""

        self._history = memento.restore()

    def perform_operation(
        self,
        operation: str,
        operand1,
        operand2,
    ) -> Decimal:
        """Perform a calculation and save history for undo."""

        # Calculate first so invalid inputs do not change history.
        calculation = Calculation.create(
            operation,
            operand1,
            operand2,
        )

        # Save the previous state before modifying history.
        self._undo_stack.append(self._create_memento())

        # A new calculation invalidates the redo history.
        self._redo_stack.clear()

        self._history.append(calculation)

        if len(self._history) > self._max_history_size:
            self._history.pop(0)

        return calculation.result

    def undo(self) -> bool:
        """Restore the previous history state."""

        if not self._undo_stack:
            return False

        # Save current state for redo.
        self._redo_stack.append(self._create_memento())

        # Restore previous state.
        previous_state = self._undo_stack.pop()
        self._restore_memento(previous_state)

        return True

    def redo(self) -> bool:
        """Restore a previously undone state."""

        if not self._redo_stack:
            return False

        # Save current state for undo.
        self._undo_stack.append(self._create_memento())

        # Restore the undone state.
        next_state = self._redo_stack.pop()
        self._restore_memento(next_state)

        return True

    def get_history(self) -> list[Calculation]:
        """Return a copy of calculation history."""

        return self._history.copy()

    def clear_history(self) -> None:
        """Clear history and save previous state for undo."""

        if not self._history:
            return  # pragma: no cover

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()
        self._history.clear()

    def get_history_count(self) -> int:
        """Return the number of calculations in history."""

        return len(self._history)