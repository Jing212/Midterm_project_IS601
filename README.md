# Advanced CLI Calculator Application

## Project Description
An enterprise-grade, interactive Command-Line Interface (REPL) calculator developed in Python. Built upon robust Object-Oriented Programming (OOP) principles, this application leverages key design patterns—including **Factory Pattern** for dynamic operation creation, **Memento Pattern** for state management (Undo/Redo capabilities), and **Observer Pattern** for automated event handling (logging and CSV persistence).

### Key Features
- **Extensible Operations**: Supports basic arithmetic as well as advanced calculations (Power, Nth Root, Modulus, Integer Division, Percentage, Absolute Difference).
- **Design Pattern Architecture**: Clean separation of concerns through Factory, Memento, and Observer patterns.
- **Undo / Redo Functionality**: Full history state tracking allowing users to step backward or forward through calculation steps.
- **Data Persistence**: Automatic and manual serialization/deserialization of calculation history to CSV using `pandas`.
- **Flexible Configuration**: Complete runtime control via environment variables (`.env`).
- **Comprehensive Logging**: Detailed multi-level system logging with customizable destinations.
- **Automated CI/CD**: Integrated GitHub Actions pipeline enforcing strict 90%+ test coverage thresholds using `pytest` and `pytest-cov`.

---

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd <YOUR_REPOSITORY_DIRECTORY>