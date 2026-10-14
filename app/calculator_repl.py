
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError


class CalculatorREPL:
    """Command-line interface for the calculator."""

    OPERATIONS = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
        "modulus",
        "int_divide",
        "percent",
        "abs_diff",
    }

    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def show_help(self) -> None:
        """Display available calculator commands."""

        print("\nAvailable Commands:")
        print("-" * 45)

        print("Arithmetic Operations:")
        for operation in sorted(self.OPERATIONS):
            print(f"  {operation} <number1> <number2>")

        print("\nHistory Commands:")
        print("  history  - Show calculation history")
        print("  clear    - Clear calculation history")
        print("  undo     - Undo the last history change")
        print("  redo     - Redo the last undone change")

        print("\nFile Commands:")
        print("  save     - Save history to CSV")
        print("  load     - Load history from CSV")

        print("\nOther Commands:")
        print("  help     - Display this help menu")
        print("  exit     - Exit the calculator")
        print("  quit     - Exit the calculator")

    def show_history(self) -> None:
        """Display calculation history."""

        history = self.calculator.get_history()

        if not history:
            print("No calculation history available.")
            return

        print("\nCalculation History:")
        print("-" * 45)

        for index, calculation in enumerate(history, start=1):
            print(
                f"{index}. "
                f"{calculation.operation} "
                f"{calculation.operand1} "
                f"{calculation.operand2} "
                f"= {calculation.result}"
            )

    def process_command(self, user_input: str) -> bool:
        """Process a command. Return False to exit."""

        parts = user_input.strip().split()

        if not parts:
            return True

        command = parts[0].lower()

        if command in ("exit", "quit"):
            if len(parts) != 1:
                print(f"Error: Usage: {command}")
                return True

            print("Goodbye!")
            return False

        if command in self.OPERATIONS:
            if len(parts) != 3:
                print(
                    f"Error: Usage: {command} "
                    "<number1> <number2>"
                )
                return True

            try:
                result = self.calculator.perform_operation(
                    command,
                    parts[1],
                    parts[2],
                )

                print(f"Result: {result}")

            except CalculatorError as error:
                print(f"Error: {error}")

            return True

        utility_commands = {
            "history",
            "clear",
            "undo",
            "redo",
            "save",
            "load",
            "help",
        }

        if command in utility_commands:
            if len(parts) != 1:
                print(f"Error: Usage: {command}")
                return True

            try:
                if command == "history":
                    self.show_history()

                elif command == "clear":
                    self.calculator.clear_history()
                    print("Calculation history cleared.")

                elif command == "undo":
                    if self.calculator.undo():
                        print("Last history change undone.")
                    else:
                        print("Nothing to undo.")

                elif command == "redo":
                    if self.calculator.redo():
                        print("Last undone change restored.")
                    else:
                        print("Nothing to redo.")

                elif command == "save":
                    path = self.calculator.save_history()
                    print(f"History saved to: {path}")

                elif command == "load":
                    count = self.calculator.load_history()
                    print(
                        f"History loaded successfully. "
                        f"{count} calculation(s) restored."
                    )

                elif command == "help":
                    self.show_help()

            except (CalculatorError, OSError) as error:
                print(f"Error: {error}")

            return True

        print(f"Unknown command: {command}")
        print("Type 'help' to see available commands.")

        return True

    def start(self) -> None:
        """Start the interactive calculator loop."""

        print("Welcome to Enhanced Python Calculator!")
        print("Type 'help' to see available commands.")

        while True:
            try:
                user_input = input("calculator> ")

                should_continue = self.process_command(
                    user_input
                )

                if not should_continue:
                    break

            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break


def main():
    config = CalculatorConfig.from_env()
    calculator = Calculator(config=config)

    try:
        repl = CalculatorREPL(calculator)
        repl.start()
    finally:
        calculator.close()


if __name__ == "__main__":
    main()
