import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation
from app.exceptions import OperationError


@pytest.fixture
def calculator():
    """Create a fresh calculator for each test."""
    return Calculator()


def test_memento_creation():
    calculation = Calculation.create("add", 10, 5)

    memento = CalculatorMemento.create([calculation])

    restored = memento.restore()

    assert len(restored) == 1
    assert restored[0].result == Decimal("15")


def test_memento_independent_copy():
    calculation = Calculation.create("add", 10, 5)

    memento = CalculatorMemento.create([calculation])

    # Modify original object after saving snapshot.
    calculation.result = Decimal("999")

    restored = memento.restore()

    assert restored[0].result == Decimal("15")


def test_memento_restore_independence():
    calculation = Calculation.create("add", 10, 5)
    memento = CalculatorMemento.create([calculation])

    first_restore = memento.restore()
    first_restore[0].result = Decimal("999")

    second_restore = memento.restore()

    assert second_restore[0].result == Decimal("15")


def test_undo_empty_history(calculator):
    assert calculator.undo() is False


def test_redo_empty_history(calculator):
    assert calculator.redo() is False


def test_undo_last_calculation(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    assert calculator.undo() is True

    history = calculator.get_history()

    assert len(history) == 1
    assert history[0].operation == "add"
    assert history[0].result == Decimal("15")


def test_redo_last_calculation(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.undo()

    assert calculator.redo() is True

    history = calculator.get_history()

    assert len(history) == 2
    assert history[-1].operation == "multiply"
    assert history[-1].result == Decimal("12")


def test_multiple_undo(calculator):
    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)

    assert calculator.undo() is True
    assert calculator.undo() is True

    history = calculator.get_history()

    assert len(history) == 1
    assert history[0].result == Decimal("2")


def test_multiple_redo(calculator):
    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)

    calculator.undo()
    calculator.undo()

    assert calculator.redo() is True
    assert calculator.redo() is True

    results = [
        calc.result for calc in calculator.get_history()
    ]

    assert results == [
        Decimal("2"),
        Decimal("4"),
        Decimal("6"),
    ]


def test_new_operation_clears_redo(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.undo()

    calculator.perform_operation("subtract", 10, 2)

    assert calculator.redo() is False

    history = calculator.get_history()

    assert len(history) == 2
    assert history[-1].operation == "subtract"


def test_failed_operation_preserves_redo(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.undo()

    with pytest.raises(OperationError):
        calculator.perform_operation("divide", 10, 0)

    # Failed calculations should not clear redo history.
    assert calculator.redo() is True

    assert calculator.get_history_count() == 2


def test_undo_clear_history(calculator):
    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.clear_history()

    assert calculator.get_history_count() == 0

    assert calculator.undo() is True
    assert calculator.get_history_count() == 2


def test_redo_clear_history(calculator):
    calculator.perform_operation("add", 10, 5)

    calculator.clear_history()
    calculator.undo()

    assert calculator.redo() is True
    assert calculator.get_history() == []


def test_undo_with_max_history_size():
    calculator = Calculator(max_history_size=2)

    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)

    assert calculator.get_history_count() == 2

    calculator.undo()

    results = [
        calc.result for calc in calculator.get_history()
    ]

    assert results == [Decimal("2"), Decimal("4")]

    calculator.redo()

    results = [
        calc.result for calc in calculator.get_history()
    ]

    assert results == [Decimal("4"), Decimal("6")]


def test_undo_redo_are_instance_specific():
    calculator1 = Calculator()
    calculator2 = Calculator()

    calculator1.perform_operation("add", 10, 5)

    assert calculator2.undo() is False
    assert calculator1.undo() is True