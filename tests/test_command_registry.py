import pytest

from app.calculator import Calculator
from app.calculator_repl import CalculatorREPL
from app.command_registry import (
    COMMAND_REGISTRY,
    register_command,
)


def test_all_operations_registered():
    assert len(COMMAND_REGISTRY) == 10

    assert "add" in COMMAND_REGISTRY
    assert "root" in COMMAND_REGISTRY
    assert "abs_diff" in COMMAND_REGISTRY


def test_registered_handler():
    calculator = Calculator()

    result = COMMAND_REGISTRY["add"].handler(
        calculator, 10, 5
    )

    assert result == 15


def test_dynamic_help(capsys):
    calculator = Calculator()
    repl = CalculatorREPL(calculator)

    repl.show_help()

    output = capsys.readouterr().out

    assert "Add two numbers" in output
    assert "Calculate absolute difference" in output


def test_new_command_updates_help(capsys):
    @register_command(
        "temporary_test_command",
        "A dynamically added test command",
    )
    def temporary_handler(calculator, a, b):
        return calculator.perform_operation("add", a, b)

    try:
        repl = CalculatorREPL(Calculator())

        repl.show_help()
        output = capsys.readouterr().out

        assert "temporary_test_command" in output
        assert "A dynamically added test command" in output

        assert repl.process_command(
            "temporary_test_command 2 3"
        ) is True

        output = capsys.readouterr().out
        assert "Result: 5" in output

    finally:
        COMMAND_REGISTRY.pop(
            "temporary_test_command", None
        )


def test_duplicate_registration():
    with pytest.raises(ValueError):

        @register_command("add", "Duplicate add")
        def duplicate_add(calculator, a, b):
            return calculator.perform_operation(
                "add", a, b
            )