# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-14

### Added
- **Complete Analysis**: Integrated dashboard combining fundamental, technical, and risk analysis.
- **GUI**: Modern PyQt6 interface with dark mode support.
- **Report Export**: Generate comprehensive PDF reports and CSV/Excel exports.
- **Data Persistence**: SQLite database to save analysis history.
- **History Tab**: View and manage past analysis results.
- **Logging**: Centralized logging system for better debugging and monitoring.
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic Oscillator, Moving Averages.
- **Fundamental Metrics**: PE, PB, ROE, Debt/Equity, Current Ratio, etc.
- **Break-Even Calculator**: Calculate break-even price with taxes and fees.
- **Tests**: Comprehensive unit test suite with high code coverage.
- **CI/CD**: GitHub Actions workflow for automated testing.
- **Docker**: Containerization support for CLI.

### Changed
- Refactored `main.py` to support new modular architecture.
- Improved code quality with type hints throughout the codebase.

### Fixed
- Fixed `pandas-ta` dependency issues.
- Resolved various linting errors and type mismatches.
