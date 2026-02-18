<div align="center">

# 📈 CSE Stock Analyzer

**A powerful stock analysis toolkit for the Colombo Stock Exchange**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-Desktop_GUI-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Tests](https://img.shields.io/badge/tests-142%20passed-brightgreen?logo=pytest&logoColor=white)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-75%25-yellowgreen)](tests/)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/MadhushanAndawaththa/CSE-Tool/releases/tag/v1.0.0)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Break-even calculations · Fee structure reference · Fundamental analysis · Technical indicators · Buy/Sell recommendations

</div>

---

## ✨ Overview

CSE Stock Analyzer is a comprehensive Python toolkit purpose-built for **Colombo Stock Exchange (CSE)** investors. It combines break-even price calculations, fundamental & technical analysis, and intelligent buy/sell recommendations — all with CSE's exact tiered fee structure baked in.

Available as a **modern desktop GUI** (PyQt6) and a **feature-rich CLI**.

---

## 🖥️ Screenshots

| Light Mode | Dark Mode |
|:---:|:---:|
| ![Light Mode](docs/screenshots/light_mode.png) | ![Dark Mode](docs/screenshots/dark_mode.png) |

> Toggle dark mode instantly from the toolbar ☀️/🌙 button or **View → Dark Mode**.

---

## 🚀 Features

### 💰 Break-Even Calculator
- Calculate the **exact minimum sell price** to recover all costs
- Includes broker commission, SEC fee, CSE fee, CDS fee, STL tax & capital gains tax
- **Profit/Loss mode** — see returns at any target selling price
- Detailed fee breakdown table with percentage analysis

### 📊 Fundamental Analysis
- **P/E Ratio** — price-to-earnings valuation
- **P/B Ratio** — price-to-book comparison
- **ROE** — return on equity performance
- **Debt-to-Equity** — leverage assessment
- **Current Ratio** — liquidity health check
- Color-coded ratings: *Excellent / Good / Fair / Poor*

### 📉 Technical Analysis
- **RSI** (Relative Strength Index) — overbought/oversold detection
- **MACD** — trend momentum & signal crossover
- **50-day & 200-day Moving Averages** — trend direction
- Interactive **price chart** with MA overlays (GUI, powered by pyqtgraph)

### 🎯 Complete Stock Analysis
- Weighted scoring combining **fundamental (60%)**, **technical (30%)**, and **risk (10%)** factors
- Actionable recommendations: *Strong Buy / Buy / Hold / Sell / Strong Sell*
- Risk assessment with confidence levels
- **PDF Report Generation**: Export beautiful analysis reports.
- **CSV/Excel Export**: Save data for further analysis.
- **Analysis History**: Auto-save and review past analyses (SQLite backed).
- Available via GUI and CLI (`python main.py` → option 3)

### 🏦 CSE Fee Structure
- Accurate **tiered fee calculation** matching official CSE rates
- Interactive fee calculator in the GUI
- Reference panel with Tier 1 & Tier 2 rate tables

### 🌗 Dark Mode
- Full dark theme support in the desktop GUI
- Theme-aware dialogs, cards, charts, and info panels
- Toggle instantly from the toolbar or View menu

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/MadhushanAndawaththa/CSE-Tool.git
cd CSE-Tool
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Quick Start

### Desktop GUI (Recommended)

```bash
python main_gui.py
```

> **Note:** If you're using a virtual environment, make sure it's activated first, or run `.venv/Scripts/python main_gui.py` directly.

### Command Line Interface

```bash
python main.py
```

The interactive menu offers:

| Option | Feature |
|:------:|---------|
| **1** | Break-Even Price Calculator |
| **2** | Fundamental Analysis |
| **3** | Complete Stock Analysis (with Recommendations) |
| **4** | View CSE Fee Structure |
| **5** | Exit |

---

## 💸 CSE Fee Structure

The tool uses CSE's official **tiered fee system**, configurable via `config.yaml`:

### Tier 1 — Transactions ≤ Rs. 100,000,000

| Fee Component | Rate |
|---------------|------|
| Broker Commission | 0.640% |
| SEC Fee | 0.072% |
| CSE Fee | 0.084% |
| CDS Fee | 0.024% |
| STL Tax *(sell only)* | 0.300% |

### Tier 2 — Transactions > Rs. 100,000,000

| Fee Component | Rate |
|---------------|------|
| Broker Commission | Min 0.200% |
| SEC Fee | 0.045% |
| CSE Fee | 0.0525% |
| CDS Fee | 0.015% |
| STL Tax *(sell only)* | 0.300% |

> **Capital Gains Tax:** 30% on net realized profit (after all fees)

---

## ⚙️ Configuration

All rates, thresholds, and scoring weights are defined in [`config.yaml`](config.yaml):

```yaml
# Customize fee rates for your broker
cse_fees:
  tier_1:
    broker_commission: 0.00640   # 0.640%
    ...

# Adjust valuation thresholds for your analysis style
thresholds:
  pe_ratio:
    undervalued: 12
    overvalued: 25

# Tune the recommendation engine weights
weights:
  fundamental: 0.60   # 60%
  technical:   0.30   # 30%
  risk:        0.10   # 10%
```

---

## 🏗️ Project Structure

```
CSE-Tool/
├── main.py                  # CLI entry point
├── main_gui.py              # GUI entry point
├── config.yaml              # Fee rates, thresholds & weights
├── pyproject.toml           # Project metadata & dependencies
├── requirements.txt         # (Legacy) Python dependencies
├── Makefile                 # Development task runner
├── Dockerfile               # Container definition
│
├── gui/                     # Desktop GUI (PyQt6)
│   ├── main_window.py       # Main window orchestration
│   ├── styles.py            # Stylesheets & themes
│   └── tabs/                # Application modules (Break-even, Fees, Fundamental, Technical, Complete, History)
│
├── src/                     # Core business logic
│   ├── analysis/            # Recommendation engine
│   ├── calculations/        # Breakeven, Fundamental, Technical math
│   ├── export/              # PDF, CSV, Excel generation
│   ├── fees/                # CSE fee logic
│   ├── storage/             # SQLite database manager
│   └── utils/               # Helpers, Logging, Validation
│
├── tests/                   # Unit tests (pytest)
├── data/                    # Database & logs
└── logs/                    # Application logs
```

---

## 🧰 Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `pandas-ta` | Technical indicators |
| `pyyaml` | Configuration loading |
| `PyQt6` | Desktop GUI framework |
| `pyqtgraph` | Interactive price charts |
| `qtawesome` | Font Awesome icons |
| `tabulate` | CLI table formatting |
| `colorama` | CLI colored output |

> **Optional:** `pyqtdarktheme` — enhanced dark mode (may not work on Python 3.12+; the app has a built-in QPalette fallback)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for CSE investors, by a CSE investor** 🇱🇰

</div>
