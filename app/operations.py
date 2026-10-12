from abc import ABC, abstractmethod
from decimal import Decimal


class Operation(ABC):

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass

class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


class Division(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

class Power(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if a == 0 and b < 0:
            raise ValueError("Zero cannot have a negative exponent.")
        if a < 0 and b != b.to_integral_value():
            raise ValueError(
                "Negative base with fractional exponent is not supported."
            )
        return a ** b


class Root(Operation):
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
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot calculate modulus by zero.")
        return a % b

class IntegerDivision(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a // b


class Percentage(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot calculate percentage with zero denominator.")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)

class OperationFactory:

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