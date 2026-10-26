"""Register calculator arithmetic commands using decorators."""

from app.command_registry import register_command


@register_command("add", "Add two numbers")
def add_command(calculator, a, b):
    """Perform addition using the calculator."""
    return calculator.perform_operation("add", a, b)


@register_command("subtract", "Subtract two numbers")
def subtract_command(calculator, a, b):
    """Perform subtraction using the calculator."""
    return calculator.perform_operation("subtract", a, b)


@register_command("multiply", "Multiply two numbers")
def multiply_command(calculator, a, b):
    """Perform multiplication using the calculator."""
    return calculator.perform_operation("multiply", a, b)


@register_command("divide", "Divide two numbers")
def divide_command(calculator, a, b):
    """Perform division using the calculator."""
    return calculator.perform_operation("divide", a, b)


@register_command("power", "Raise a number to a power")
def power_command(calculator, a, b):
    """Perform power using the calculator."""
    return calculator.perform_operation("power", a, b)


@register_command("root", "Calculate the nth root")
def root_command(calculator, a, b):
    """Perform root calculation using the calculator."""
    return calculator.perform_operation("root", a, b)


@register_command("modulus", "Calculate the remainder")
def modulus_command(calculator, a, b):
    """Perform modulus using the calculator."""
    return calculator.perform_operation("modulus", a, b)


@register_command("int_divide", "Perform integer division")
def int_divide_command(calculator, a, b):
    """Perform integer division using the calculator."""
    return calculator.perform_operation("int_divide", a, b)


@register_command("percent", "Calculate percentage")
def percent_command(calculator, a, b):
    """Perform percentage calculation using the calculator."""
    return calculator.perform_operation("percent", a, b)


@register_command("abs_diff", "Calculate absolute difference")
def abs_diff_command(calculator, a, b):
    """Perform absolute difference calculation using the calculator."""
    return calculator.perform_operation("abs_diff", a, b)
