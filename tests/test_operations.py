import pytest
from decimal import Decimal

from app.operations import (
    Operation,
    OperationFactory,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
)


@pytest.mark.parametrize(
    "operation_class, a, b, expected",
    [
        (Addition, "10", "5", "15"),
        (Subtraction, "10", "5", "5"),
        (Multiplication, "10", "5", "50"),
        (Division, "10", "5", "2"),
        (Power, "2", "3", "8"),
        (Root, "27", "3", "3"),
        (Modulus, "10", "3", "1"),
        (IntegerDivision, "10", "3", "3"),
        (Percentage, "25", "100", "25"),
        (AbsoluteDifference, "5", "12", "7"),
    ],
)
def test_operations(operation_class, a, b, expected):
    operation = operation_class()

    result = operation.execute(
        Decimal(a),
        Decimal(b)
    )

    assert result == pytest.approx(Decimal(expected))


def test_factory_creates_correct_operation():
    operation = OperationFactory.create_operation("add")

    assert isinstance(operation, Addition)
    assert isinstance(operation, Operation)


def test_factory_invalid_operation():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown")


@pytest.mark.parametrize(
    "operation_class",
    [Division, Modulus, IntegerDivision, Percentage],
)
def test_zero_denominator(operation_class):
    operation = operation_class()

    with pytest.raises(ValueError):
        operation.execute(Decimal("10"), Decimal("0"))


def test_negative_exponent():
    operation = Power()

    assert operation.execute(
        Decimal("2"), Decimal("-2")
    ) == Decimal("0.25")


def test_invalid_zero_negative_power():
    with pytest.raises(ValueError):
        Power().execute(Decimal("0"), Decimal("-1"))


def test_negative_odd_root():
    result = Root().execute(Decimal("-8"), Decimal("3"))

    assert result == pytest.approx(Decimal("-2"))


def test_invalid_even_root():
    with pytest.raises(ValueError):
        Root().execute(Decimal("-16"), Decimal("2"))


def test_invalid_root_degree():
    with pytest.raises(ValueError):
        Root().execute(Decimal("9"), Decimal("0"))