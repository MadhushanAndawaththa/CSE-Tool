"""
Shared fixtures for CSE Stock Analyzer tests.
"""

import pytest
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def sample_config() -> dict:
    """Provide a deterministic test configuration (matches default config.yaml)."""
    return {
        'cse_fees': {
            'tier_1': {
                'max_value': 100_000_000,
                'broker_commission': 0.00640,
                'cse_fee': 0.00084,
                'cds_fee': 0.00024,
                'sec_fee': 0.00072,
                'stl_tax': 0.003,
            },
            'tier_2': {
                'min_value': 100_000_000,
                'broker_commission': 0.002000,
                'cse_fee': 0.000525,
                'cds_fee': 0.000150,
                'sec_fee': 0.000450,
                'stl_tax': 0.003,
            },
            'minimum_commission': 100,
        },
        'taxes': {
            'capital_gains_tax': 0.30,
            'dividend_withholding': 0.14,
        },
        'thresholds': {
            'pe_ratio': {'undervalued': 12, 'fair_value_min': 12, 'fair_value_max': 18, 'overvalued': 25},
            'pb_ratio': {'undervalued': 1.0, 'fair_value': 1.5, 'overvalued': 3.0},
            'roe': {'excellent': 0.20, 'good': 0.15, 'acceptable': 0.10, 'poor': 0.05},
            'debt_to_equity': {'conservative': 0.5, 'moderate': 1.0, 'aggressive': 1.5, 'risky': 2.0},
            'current_ratio': {'strong': 2.0, 'adequate': 1.5, 'concerning': 1.0},
            'earnings_growth': {'excellent': 0.20, 'good': 0.10, 'moderate': 0.05},
            'rsi': {'oversold': 30, 'neutral_low': 40, 'neutral_high': 60, 'overbought': 70},
            'weights': {'fundamental': 0.60, 'technical': 0.30, 'risk': 0.10},
        },
    }


@pytest.fixture
def sample_stock_data() -> dict:
    """Provide sample stock data for fundamental analysis."""
    return {
        'ticker': 'JKH',
        'company_name': 'John Keells Holdings',
        'price': 161.25,
        'eps': 12.50,
        'book_value_per_share': 85.00,
        'net_income': 5_000_000_000,
        'shareholders_equity': 25_000_000_000,
        'total_debt': 10_000_000_000,
        'current_assets': 15_000_000_000,
        'current_liabilities': 8_000_000_000,
    }


@pytest.fixture
def sample_prices() -> list[float]:
    """Provide 50 historical prices for technical analysis."""
    return [
        150.00, 152.50, 151.00, 153.75, 155.00, 154.25, 156.50, 158.00,
        157.00, 159.25, 160.50, 161.00, 160.25, 162.00, 163.50, 162.75,
        164.00, 165.50, 164.25, 166.00, 167.50, 168.00, 167.25, 169.00,
        170.50, 169.75, 171.00, 172.50, 171.25, 173.00, 174.50, 173.75,
        175.00, 176.50, 175.25, 177.00, 178.50, 177.75, 179.00, 180.50,
        179.75, 181.00, 182.50, 181.25, 183.00, 184.50, 183.75, 185.00,
        186.50, 185.25,
    ]


@pytest.fixture
def uptrend_prices() -> list[float]:
    """Prices in a clear uptrend for technical indicator tests."""
    base = 100.0
    return [base + i * 0.5 + ((-1) ** i) * 0.3 for i in range(60)]


@pytest.fixture
def downtrend_prices() -> list[float]:
    """Prices in a clear downtrend for technical indicator tests."""
    base = 200.0
    return [base - i * 0.5 + ((-1) ** i) * 0.3 for i in range(60)]
