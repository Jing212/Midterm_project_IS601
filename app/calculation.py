from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from app.operations import OperationFactory
from app.exceptions import OperationError
from app.input_validators import InputValidator


@dataclass
class Calculation:
    """Represent a single calculator operation."""

    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def create(
        cls,
        operation: str,
        operand1,
        operand2,
        max_value=Decimal("1000000"),
    ):
        """Validate inputs, perform the operation, and create a record."""

        a = InputValidator.validate_number(operand1, max_value)
        b = InputValidator.validate_number(operand2, max_value)

        if not isinstance(operation, str):
            raise OperationError("Operation name must be a string.")

        operation_name = operation.lower().strip()

        try:
            strategy = OperationFactory.create_operation(operation_name)
            result = strategy.execute(a, b)

        except (ValueError, ArithmeticError, OverflowError) as error:
            raise OperationError(str(error)) from error

        try:
            result = Decimal(str(result))
        except (InvalidOperation, ValueError, TypeError) as error:
            raise OperationError("Invalid calculation result.") from error

        if not result.is_finite():
            raise OperationError("Calculation produced a non-finite result.")

        return cls(
            operation=operation_name,
            operand1=a,
            operand2=b,
            result=result,
        )

    def to_dict(self) -> dict:
        """Convert Calculation into a dictionary."""

        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Restore a Calculation object from a dictionary."""

        try:
            return cls(
                operation=data["operation"],
                operand1=Decimal(str(data["operand1"])),
                operand2=Decimal(str(data["operand2"])),
                result=Decimal(str(data["result"])),
                timestamp=datetime.fromisoformat(data["timestamp"]),
            )
        except (KeyError, TypeError, ValueError, InvalidOperation) as error:
            raise OperationError(
                "Invalid calculation history data."
            ) from error