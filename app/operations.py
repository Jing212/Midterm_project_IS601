"""Implement calculator arithmetic strategies and factory."""

from abc import ABC, abstractmethod
from decimal import Decimal


class Operation(ABC):
    """Abstract base class for arithmetic operations."""
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Execute the arithmetic operation using two operands."""
        pass

class Addition(Operation):
    """Perform addition of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


class Subtraction(Operation):
    """Perform subtraction of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


class Multiplication(Operation):
    """Perform multiplication of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


class Division(Operation):
    """Perform division of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

class Power(Operation):
    """Perform exponentiation of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if a == 0 and b < 0:
            raise ValueError("Zero cannot have a negative exponent.")
        if a < 0 and b != b.to_integral_value():
            raise ValueError(
                "Negative base with fractional exponent is not supported."
            )
        return a ** b


class Root(Operation):
    """Calculate the nth root of a number."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Root degree cannot be zero.")

        if b != b.to_integral_value():
            raise ValueError("Root degree must be an integer.")

        degree = int(b)

        if a < 0:
            if degree % 2 == 0:
                raise ValueError("Even root of a negative number is invalid.")

            return -((-a) ** (Decimal(1) / b))

        if a == 0 and degree < 0:
            raise ValueError("Cannot take a negative root of zero.")

        return a ** (Decimal(1) / b)


class Modulus(Operation):
    """Calculate the modulus of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot calculate modulus by zero.")
        return a % b

class IntegerDivision(Operation):
    """Perform integer division of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a // b


class Percentage(Operation):
    """Calculate the percentage of two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot calculate percentage with zero denominator.")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculate the absolute difference between two numbers."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)

class OperationFactory:
    """Create arithmetic operation strategies by name."""
    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivision,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        operation_class = cls._operations.get(operation_name.lower())

        if operation_class is None:
            raise ValueError(
                f"Unsupported operation: {operation_name}"
            )

        return operation_class()
