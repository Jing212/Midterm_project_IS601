from decimal import Decimal

from app.calculation import Calculation
from app.exceptions import ValidationError


class Calculator:
    """Manage calculations and calculation history."""

    def __init__(self, max_history_size: int = 100):
        """Initialize the calculator."""

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

    def perform_operation(
        self,
        operation: str,
        operand1,
        operand2,
    ) -> Decimal:
        """Perform a calculation and save it to history."""

        calculation = Calculation.create(
            operation,
            operand1,
            operand2,
        )

        self._history.append(calculation)

        if len(self._history) > self._max_history_size:
            self._history.pop(0)

        return calculation.result

    def get_history(self) -> list[Calculation]:
        """Return a copy of the calculation history."""

        return self._history.copy()

    def clear_history(self) -> None:
        """Remove all calculations from history."""

        self._history.clear()

    def get_history_count(self) -> int:
        """Return the number of saved calculations."""

        return len(self._history)