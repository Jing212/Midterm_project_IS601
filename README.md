# Enhanced Python Calculator

## Project Overview
A command-line calculator built using Python and OOP design patterns.

## Features
- Ten arithmetic operations
- Strategy and Factory Patterns
- Memento Pattern for Undo/Redo
- Observer Pattern for logging and auto-save
- Decorator-based Dynamic Help Menu
- CSV history persistence using pandas
- Environment configuration using python-dotenv

## Installation
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

## Configuration
Create a .env file and configure calculator settings.

## Running the Calculator
python -m app.calculator_repl

## Avalable REPL Commands
- `add <num1> <num2>`: Add two numbers
- `subtract <num1> <num2>`: Subtract two numbers
- `multiply <num1> <num2>`: Multiply two numbers
- `divide <num1> <num2>`: Divide two numbers
- `undo`: Undo the last operation
- `redo`: Redo the last undone operation
- `history`: Show operation history
- `clear_history`: Clear operation history
- `help`: Show help menu

## History Management
View calculation history in CSV format. History is automatically saved to a file specified in the configuration.

Undo and redo operations are supported, allowing users to revert or reapply previous calculations.

Clear calculation history with the `clear_history` command.

CSV File Persistence: The calculator saves the history of operations to a CSV file using pandas. The file path can be configured in the .env file.

Display the help menu with the `help` command, which lists all available commands and their descriptions.

Exit the calculator by typing `exit` or pressing Ctrl+C.

## Logging
The application uses Python's built-in logging module to log operations, errors, and other significant events. Logs are saved to a file specified in the configuration.

## Testing
python -m pytest tests/ -v

## Coverage
python -m pytest tests/ --cov=app --cov-fail-under=90

## Continuous Integration
GitHub Actions runs tests and enforces 90% coverage
on pushes and pull requests to main.

## Optional Enhancement
Dynamic Help Menu implemented with the Decorator Pattern.