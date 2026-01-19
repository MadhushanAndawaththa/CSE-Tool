# CSE Stock Analysis & Break-Even Calculator

A comprehensive Python tool for analyzing Colombo Stock Exchange (CSE) stocks with break-even price calculations, fundamental analysis, technical indicators, and buy/sell recommendations. Available in both **CLI** and **Desktop GUI** versions.

## Features

- **Break-Even Calculator**: Calculate the exact price needed to break even after all CSE fees and taxes
- **Profit/Loss Analysis**: Calculate profit/loss at specific selling prices
- **Fundamental Analysis**: P/E ratio, P/B ratio, ROE, Debt-to-Equity, Current Ratio, Earnings Growth
- **Technical Indicators**: RSI, MACD, 50-day & 200-day Moving Averages
- **Buy/Sell Recommendations**: Weighted scoring system combining fundamental, technical, and risk analysis
- **CSE-Specific Fees**: Accurate calculation of broker commission, SEC fee, STL tax, and capital gains tax
- **Desktop GUI**: Modern PyQt6 interface with interactive forms and visual results

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Desktop GUI (Recommended)
```bash
python main_gui.py
```

### Command Line Interface
```bash
# Interactive menu
python main.py

# Or use the CLI directly (coming soon)
python main.py breakeven
```

## CSE Fee Structure (Tiered System)

### Tier 1: Transactions ≤ Rs. 100,000,000
- **Broker Commission**: 0.64%
- **SEC Fee**: 0.072%
- **CSE Fee**: 0.084%
- **CDS Fee**: 0.024%
- **STL Tax**: 0.3% (on sell only)
- **Total Buy Fees**: ~0.82%
- **Total Sell Fees**: ~1.12%

### Tier 2: Transactions > Rs. 100,000,000
- **Broker Commission**: Min 0.20%
- **SEC Fee**: 0.042%
- **CSE Fee**: 0.054%
- **CDS Fee**: 0.024%
- **STL Tax**: 0.3% (on sell only)
- **Total Buy Fees**: ~0.36%
- **Total Sell Fees**: ~0.66%

**Capital Gains Tax**: 30% on net profit (after fees)

## Configuration

Edit `config.yaml` to customize:
- Fee rates (for different brokers)
- Valuation thresholds
- Scoring weights (fundamental vs technical)

## Usage Examples

### Desktop GUI
1. Launch the application: `python main_gui.py`
2. Navigate between tabs for different features
3. **Break-Even Calculator Tab**: Enter buy price, quantity, and optionally a sell price
4. **Fee Information Tab**: Calculate fees for any transaction value
5. Results are displayed in formatted tables with color-coded profit/loss indicators

### Command Line Interface

### Break-Even Calculation
```bash
python main.py breakeven
# Enter: Buy price, quantity, purchase date
# Output: Minimum sell price to break even
```

### Full Stock Analysis
```bash
python main.py analyze
# Enter: All stock data (price, financials, historical prices)
# Output: Complete analysis with buy/sell/hold recommendation
```

### Quick Fundamental Analysis
```bash
python main.py fundamental
# Enter: Price, EPS, Book Value, ROE, etc.
# Output: Fundamental scores and ratios
```

## Requirements

### Core Dependencies
- Python 3.9+
- pandas, numpy
- pandas-ta (for technical indicators)
- pyyaml (for configuration)

### CLI Version
- colorama (for colored output)
- tabulate (for formatted tables)
- click (for CLI)

### Desktop GUI Version
- PyQt6 (for GUI framework)
- matplotlib (for charts)
- reportlab (for PDF export)

## License

MIT License
