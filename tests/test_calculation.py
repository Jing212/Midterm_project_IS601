import pytest
from decimal import Decimal
from datetime import datetime

from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError


def test_create_calculation():
    calc = Calculation.create("add", 10, 5)

    assert calc.operation == "add"
    assert calc.operand1 == Decimal("10")
    assert calc.operand2 == Decimal("5")
    assert calc.result == Decimal("15")
    assert isinstance(calc.timestamp, datetime)


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("add", "10", "5", "15"),
        ("subtract", "10", "5", "5"),
        ("multiply", "10", "5", "50"),
        ("divide", "10", "5", "2"),
        ("power", "2", "3", "8"),
        ("modulus", "10", "3", "1"),
        ("percent", "25", "100", "25"),
        ("abs_diff", "5", "12", "7"),
        ("int_divide", "10", "3", "3"),
    ],
)
def test_calculation_operations(operation, a, b, expected):
    calc = Calculation.create(operation, a, b)

    assert calc.result == Decimal(expected)


def test_calculation_root():
    calc = Calculation.create("root", 27, 3)

    assert float(calc.result) == pytest.approx(3.0)


def test_calculation_to_dict():
    calc = Calculation.create("add", 10, 5)

    data = calc.to_dict()

    assert data["operation"] == "add"
    assert data["operand1"] == "10"
    assert data["operand2"] == "5"
    assert data["result"] == "15"
    assert "timestamp" in data


def test_calculation_from_dict():
    original = Calculation.create("multiply", 6, 7)

    data = original.to_dict()
    restored = Calculation.from_dict(data)

    assert restored.operation == original.operation
    assert restored.result == Decimal("42")
    assert restored.timestamp == original.timestamp


def test_division_by_zero():
    with pytest.raises(OperationError):
        Calculation.create("divide", 10, 0)


def test_invalid_operation():
    with pytest.raises(OperationError):
        Calculation.create("unknown", 10, 5)


def test_invalid_input():
    with pytest.raises(ValidationError):
        Calculation.create("add", "abc", 5)


def test_invalid_history_data():
    with pytest.raises(OperationError):
        Calculation.from_dict({"operation": "add"})


def test_non_string_operation():
    with pytest.raises(OperationError):
        Calculation.create(123, 10, 5)