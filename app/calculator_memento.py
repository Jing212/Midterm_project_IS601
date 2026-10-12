from dataclasses import dataclass
from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    """Store a snapshot of calculator history."""

    _history: tuple[Calculation, ...]

    @classmethod
    def create(cls, history: list[Calculation]):
        """Create a snapshot of the current history."""

        snapshots = tuple(
            Calculation.from_dict(calc.to_dict())
            for calc in history
        )

        return cls(_history=snapshots)

    def restore(self) -> list[Calculation]:
        """Restore a separate copy of the saved history."""

        return [
            Calculation.from_dict(calc.to_dict())
            for calc in self._history
        ]