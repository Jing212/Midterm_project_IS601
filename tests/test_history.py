import logging
from decimal import Decimal

import pandas as pd
import pytest

from app.calculation import Calculation
from app.calculator import Calculator
from app.history import (
    HistoryObserver,
    LoggingObserver,
    AutoSaveObserver,
)


class MockObserver(HistoryObserver):
    """A simple observer used to verify notifications."""

    def __init__(self):
        self.events = []

    def update(self, event, calculation, history):
        self.events.append(
            (event, calculation, history)
        )


@pytest.fixture
def calculator():
    return Calculator()


def test_register_observer(calculator):
    observer = MockObserver()

    calculator.register_observer(observer)
    calculator.perform_operation("add", 10, 5)

    assert len(observer.events) == 1

    event, calculation, history = observer.events[0]

    assert event == "calculation"
    assert calculation.result == Decimal("15")
    assert len(history) == 1


def test_multiple_observers(calculator):
    observer1 = MockObserver()
    observer2 = MockObserver()

    calculator.register_observer(observer1)
    calculator.register_observer(observer2)

    calculator.perform_operation("multiply", 4, 3)

    assert len(observer1.events) == 1
    assert len(observer2.events) == 1


def test_duplicate_registration(calculator):
    observer = MockObserver()

    calculator.register_observer(observer)
    calculator.register_observer(observer)

    calculator.perform_operation("add", 1, 2)

    assert len(observer.events) == 1


def test_remove_observer(calculator):
    observer = MockObserver()

    calculator.register_observer(observer)
    calculator.remove_observer(observer)

    calculator.perform_operation("add", 10, 5)

    assert observer.events == []


def test_invalid_observer(calculator):
    with pytest.raises(TypeError):
        calculator.register_observer(object())


def test_failed_calculation_does_not_notify(calculator):
    observer = MockObserver()
    calculator.register_observer(observer)

    with pytest.raises(Exception):
        calculator.perform_operation("divide", 10, 0)

    assert observer.events == []


def test_logging_observer(tmp_path):
    log_file = tmp_path / "logs" / "calculator.log"

    observer = LoggingObserver(log_file)

    calculator = Calculator()
    calculator.register_observer(observer)

    calculator.perform_operation("add", 10, 5)
    observer.close()

    content = log_file.read_text(encoding="utf-8")

    assert "INFO" in content
    assert "add" in content
    assert "10" in content
    assert "5" in content
    assert "15" in content


def test_logging_ignores_other_events(tmp_path):
    log_file = tmp_path / "calculator.log"

    observer = LoggingObserver(log_file)
    observer.update("undo", None, [])
    observer.close()

    assert log_file.read_text(encoding="utf-8") == ""


def test_autosave_observer(tmp_path):
    csv_file = tmp_path / "history" / "calculations.csv"

    observer = AutoSaveObserver(csv_file, enabled=True)

    calculator = Calculator()
    calculator.register_observer(observer)

    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    assert csv_file.exists()

    df = pd.read_csv(csv_file)

    assert len(df) == 2
    assert df["operation"].tolist() == ["add", "multiply"]
    assert df["result"].tolist() == [15, 12]


def test_autosave_disabled(tmp_path):
    csv_file = tmp_path / "history.csv"

    observer = AutoSaveObserver(csv_file, enabled=False)

    calculator = Calculator()
    calculator.register_observer(observer)

    calculator.perform_operation("add", 10, 5)

    assert not csv_file.exists()


def test_autosave_ignores_unknown_events(tmp_path):
    csv_file = tmp_path / "history.csv"

    observer = AutoSaveObserver(csv_file)
    observer.update("unknown_event", None, [])

    assert not csv_file.exists()


def test_autosave_respects_max_history_size(tmp_path):
    csv_file = tmp_path / "history.csv"

    calculator = Calculator(max_history_size=2)
    calculator.register_observer(AutoSaveObserver(csv_file))

    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)

    df = pd.read_csv(csv_file)

    assert len(df) == 2
    assert df["result"].tolist() == [4, 6]


def test_observer_receives_updated_history(calculator):
    observer = MockObserver()
    calculator.register_observer(observer)

    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("subtract", 10, 3)

    first_event = observer.events[0]
    second_event = observer.events[1]

    assert len(first_event[2]) == 1
    assert len(second_event[2]) == 2