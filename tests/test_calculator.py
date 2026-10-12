import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.calculation import Calculation
from app.exceptions import (
    ValidationError,
    OperationError,
)


@pytest.fixture
def calculator():
    """Create a fresh calculator for each test."""
    return Calculator()


def test_calculator_initialization(calculator):
    assert calculator.get_history() == []
    assert calculator.get_history_count() == 0


def test_perform_addition(calculator):
    result = calculator.perform_operation("add", 10, 5)

    assert result == Decimal("15")


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("add", 10, 5, "15"),
        ("subtract", 10, 5, "5"),
        ("multiply", 10, 5, "50"),
        ("divide", 10, 5, "2"),
        ("power", 2, 3, "8"),
        ("modulus", 10, 3, "1"),
        ("int_divide", 10, 3, "3"),
        ("percent", 25, 100, "25"),
        ("abs_diff", 5, 12, "7"),
    ],
)
def test_calculator_operations(calculator, operation, a, b, expected):
    result = calculator.perform_operation(operation, a, b)

    assert result == Decimal(expected)


def test_root_operation(calculator):
    result = calculator.perform_operation("root", 27, 3)

    assert float(result) == pytest.approx(3.0)


def test_history_saves_calculations(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    history = calculator.get_history()

    assert len(history) == 2
    assert isinstance(history[0], Calculation)
    assert history[0].operation == "add"
    assert history[0].result == Decimal("15")
    assert history[1].operation == "multiply"
    assert history[1].result == Decimal("12")


def test_history_count(calculator):
    assert calculator.get_history_count() == 0

    calculator.perform_operation("add", 10, 5)

    assert calculator.get_history_count() == 1


def test_clear_history(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("subtract", 8, 3)

    calculator.clear_history()

    assert calculator.get_history() == []
    assert calculator.get_history_count() == 0


def test_max_history_size():
    calculator = Calculator(max_history_size=2)

    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)

    history = calculator.get_history()

    assert len(history) == 2
    assert history[0].result == Decimal("4")
    assert history[1].result == Decimal("6")


def test_history_returns_copy(calculator):
    calculator.perform_operation("add", 10, 5)

    history = calculator.get_history()
    history.clear()

    assert calculator.get_history_count() == 1


@pytest.mark.parametrize(
    "size",
    [0, -1, 1.5, "100", True, None],
)
def test_invalid_max_history_size(size):
    with pytest.raises(ValidationError):
        Calculator(max_history_size=size)


def test_division_by_zero_does_not_change_history(calculator):
    with pytest.raises(OperationError):
        calculator.perform_operation("divide", 10, 0)

    assert calculator.get_history_count() == 0


def test_invalid_input_does_not_change_history(calculator):
    with pytest.raises(ValidationError):
        calculator.perform_operation("add", "abc", 5)

    assert calculator.get_history_count() == 0


def test_invalid_operation_does_not_change_history(calculator):
    with pytest.raises(OperationError):
        calculator.perform_operation("unknown", 10, 5)

    assert calculator.get_history_count() == 0


def test_calculator_instances_have_separate_histories():
    calculator1 = Calculator()
    calculator2 = Calculator()

    calculator1.perform_operation("add", 10, 5)

    assert calculator1.get_history_count() == 1
    assert calculator2.get_history_count() == 0