# Contributing to CSE Stock Analyzer

Thank you for your interest in contributing to the CSE Stock Analyzer! We welcome contributions from the community to make this tool better for everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/cse-stock-analyzer.git
    cd cse-stock-analyzer
    ```
3.  **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -e .[dev]
    ```

## Development Workflow

1.  Create a new branch for your feature or fix:
    ```bash
    git checkout -b feature/amazing-feature
    ```
2.  Make your changes.
3.  Run tests to ensure nothing is broken:
    ```bash
    pytest
    ```
4.  Ensure your code follows the style guidelines (we use Black, isort, and Flake8).

## Pull Request Process

1.  Update the `README.md` and `CHANGELOG.md` with details of changes.
2.  Push your branch to GitHub.
3.  Open a Pull Request against the `main` branch.
4.  The CI pipeline will run to verify your changes.

## Coding Standards

-   **Type Hints**: All new code must have type annotations.
-   **Docstrings**: All modules, classes, and functions should have docstrings.
-   **Tests**: Add unit tests for new functionality.
-   **Style**: Follow PEP 8 guidelines.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub describing the problem or idea in detail.
