import pytest

from app.calculator import Calculator
from app.calculator_repl import CalculatorREPL


@pytest.fixture
def repl():
    calculator = Calculator()
    return CalculatorREPL(calculator)


@pytest.mark.parametrize(
    "command, expected",
    [
        ("add 10 5", "15"),
        ("subtract 10 5", "5"),
        ("multiply 4 3", "12"),
        ("divide 10 5", "2"),
        ("power 2 3", "8"),
        ("modulus 10 3", "1"),
        ("int_divide 10 3", "3"),
        ("percent 25 100", "25"),
        ("abs_diff 5 12", "7"),
    ],
)
def test_operations(repl, capsys, command, expected):
    assert repl.process_command(command) is True

    output = capsys.readouterr().out

    assert f"Result: {expected}" in output


def test_root(repl, capsys):
    repl.process_command("root 27 3")

    output = capsys.readouterr().out

    assert "Result: 3" in output


def test_invalid_argument_count(repl, capsys):
    assert repl.process_command("add 10") is True

    output = capsys.readouterr().out

    assert "Usage" in output


def test_invalid_number(repl, capsys):
    assert repl.process_command("add abc 5") is True

    output = capsys.readouterr().out

    assert "Error:" in output


def test_division_by_zero(repl, capsys):
    assert repl.process_command("divide 10 0") is True

    output = capsys.readouterr().out

    assert "Error:" in output


def test_unknown_command(repl, capsys):
    assert repl.process_command("hello") is True

    output = capsys.readouterr().out

    assert "Unknown command" in output


def test_exit(repl, capsys):
    assert repl.process_command("exit") is False

    output = capsys.readouterr().out

    assert "Goodbye!" in output


def test_empty_input(repl):
    assert repl.process_command("   ") is True


def test_case_insensitive_command(repl, capsys):
    assert repl.process_command("ADD 10 5") is True

    output = capsys.readouterr().out

    assert "Result: 15" in output


def test_help_command(repl, capsys):
    assert repl.process_command("help") is True

    output = capsys.readouterr().out

    assert "Available Commands" in output
    assert "add" in output
    assert "undo" in output
    assert "save" in output


def test_history_empty(repl, capsys):
    repl.process_command("history")

    output = capsys.readouterr().out

    assert "No calculation history available." in output


def test_history_with_calculations(repl, capsys):
    repl.process_command("add 10 5")
    repl.process_command("multiply 4 3")

    capsys.readouterr()

    repl.process_command("history")

    output = capsys.readouterr().out

    assert "1. add 10 5 = 15" in output
    assert "2. multiply 4 3 = 12" in output


def test_clear_command(repl, capsys):
    repl.process_command("add 10 5")
    repl.process_command("clear")

    assert repl.calculator.get_history_count() == 0

    output = capsys.readouterr().out
    assert "Calculation history cleared." in output


def test_undo_command(repl, capsys):
    repl.process_command("add 10 5")
    repl.process_command("multiply 4 3")

    repl.process_command("undo")

    assert repl.calculator.get_history_count() == 1

    output = capsys.readouterr().out
    assert "undone" in output


def test_redo_command(repl, capsys):
    repl.process_command("add 10 5")
    repl.process_command("undo")
    repl.process_command("redo")

    assert repl.calculator.get_history_count() == 1

    output = capsys.readouterr().out
    assert "restored" in output


def test_undo_when_empty(repl, capsys):
    repl.process_command("undo")

    output = capsys.readouterr().out
    assert "Nothing to undo." in output


def test_redo_when_empty(repl, capsys):
    repl.process_command("redo")

    output = capsys.readouterr().out
    assert "Nothing to redo." in output


def test_save_command(repl, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    repl.process_command("add 10 5")
    repl.process_command("save")

    csv_file = (
        tmp_path / "history" / "calculator_history.csv"
    )

    assert csv_file.exists()

    output = capsys.readouterr().out
    assert "History saved to:" in output


def test_load_command(repl, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    repl.process_command("add 10 5")
    repl.process_command("save")

    # Use undo instead of clear, since the unconfigured
    # test calculator does not auto-save on undo.
    repl.process_command("undo")

    assert repl.calculator.get_history_count() == 0

    repl.process_command("load")

    assert repl.calculator.get_history_count() == 1

    output = capsys.readouterr().out
    assert "History loaded successfully." in output


def test_load_missing_file(repl, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    repl.process_command("load")

    output = capsys.readouterr().out
    assert "Error:" in output


def test_utility_command_extra_arguments(repl, capsys):
    repl.process_command("undo 10")

    output = capsys.readouterr().out

    assert "Usage: undo" in output


def test_quit_command(repl, capsys):
    assert repl.process_command("quit") is False

    output = capsys.readouterr().out

    assert "Goodbye!" in output
