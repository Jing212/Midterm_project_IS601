from decimal import Decimal

import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


@pytest.fixture
def configured_calculator(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        log_file="calculator.log",
        history_file="calculations.csv",
        max_history_size=10,
        auto_save=True,
        precision=4,
        max_input_value=Decimal("1000"),
        default_encoding="utf-8",
    )

    calculator = Calculator(config=config)

    yield calculator

    calculator.close()


def test_auto_registration(configured_calculator):
    calculator = configured_calculator

    calculator.perform_operation("add", 10, 5)

    assert calculator.config.history_path.exists()
    assert calculator.config.log_path.exists()


def test_precision(configured_calculator):
    result = configured_calculator.perform_operation(
        "divide", 10, 3
    )

    assert result == Decimal("3.3333")


def test_max_input_value(configured_calculator):
    with pytest.raises(ValidationError):
        configured_calculator.perform_operation(
            "add", 1001, 1
        )


def test_save_history(configured_calculator, tmp_path):
    calculator = configured_calculator
    calculator.perform_operation("add", 10, 5)

    file = tmp_path / "manual.csv"
    calculator.save_history(file)

    assert file.exists()

    df = pd.read_csv(file)
    assert len(df) == 1
    assert df["operation"].iloc[0] == "add"


def test_load_history(configured_calculator, tmp_path):
    calculator = configured_calculator
    calculator.perform_operation("multiply", 6, 7)

    backup = tmp_path / "backup.csv"
    calculator.save_history(backup)

    calculator.clear_history()
    assert calculator.get_history_count() == 0

    count = calculator.load_history(backup)

    assert count == 1
    assert calculator.get_history()[0].result == Decimal("42")


def test_undo_syncs_csv(configured_calculator):
    calculator = configured_calculator

    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.undo()

    df = pd.read_csv(calculator.config.history_path)

    assert len(df) == 1
    assert df["operation"].iloc[0] == "add"


def test_redo_syncs_csv(configured_calculator):
    calculator = configured_calculator

    calculator.perform_operation("add", 10, 5)
    calculator.perform_operation("multiply", 4, 3)

    calculator.undo()
    calculator.redo()

    df = pd.read_csv(calculator.config.history_path)

    assert len(df) == 2
    assert df["operation"].tolist() == [
        "add",
        "multiply",
    ]


def test_clear_syncs_csv(configured_calculator):
    calculator = configured_calculator

    calculator.perform_operation("add", 10, 5)
    calculator.clear_history()

    df = pd.read_csv(calculator.config.history_path)

    assert df.empty
    assert list(df.columns) == Calculator.COLUMNS


def test_invalid_csv_preserves_history(
    configured_calculator, tmp_path
):
    calculator = configured_calculator
    calculator.perform_operation("add", 10, 5)

    invalid_file = tmp_path / "invalid.csv"
    invalid_file.write_text(
        "wrong,column\n1,2\n",
        encoding="utf-8",
    )

    with pytest.raises(OperationError):
        calculator.load_history(invalid_file)

    assert calculator.get_history_count() == 1
    assert calculator.get_history()[0].result == Decimal("15")


def test_missing_csv(configured_calculator, tmp_path):
    with pytest.raises(OperationError):
        configured_calculator.load_history(
            tmp_path / "missing.csv"
        )


def test_load_can_be_undone(configured_calculator, tmp_path):
    calculator = configured_calculator

    calculator.perform_operation("add", 10, 5)

    backup = tmp_path / "backup.csv"
    calculator.save_history(backup)

    calculator.perform_operation("multiply", 4, 3)
    assert calculator.get_history_count() == 2

    calculator.load_history(backup)
    assert calculator.get_history_count() == 1

    calculator.undo()

    assert calculator.get_history_count() == 2