"""Tests for src.utils.helpers module."""

import pytest
from src.utils.helpers import (
    format_currency,
    format_percentage,
    validate_positive_number,
    validate_non_negative_number,
    load_config,
    get_data_dir,
)


# ── format_currency ──────────────────────────────────────────────────

class TestFormatCurrency:
    def test_basic(self):
        assert format_currency(1000) == "LKR 1,000.00"

    def test_large_number(self):
        assert format_currency(1_234_567.89) == "LKR 1,234,567.89"

    def test_small_number(self):
        assert format_currency(0.50) == "LKR 0.50"

    def test_custom_currency(self):
        assert format_currency(100, currency="USD") == "USD 100.00"

    def test_negative(self):
        assert format_currency(-500) == "LKR -500.00"

    def test_zero(self):
        assert format_currency(0) == "LKR 0.00"


# ── format_percentage ────────────────────────────────────────────────

class TestFormatPercentage:
    def test_basic(self):
        assert format_percentage(0.1525) == "15.25%"

    def test_zero(self):
        assert format_percentage(0) == "0.00%"

    def test_negative(self):
        assert format_percentage(-0.05) == "-5.00%"

    def test_custom_decimals(self):
        assert format_percentage(0.12345, decimal_places=3) == "12.345%"


# ── validate_positive_number ─────────────────────────────────────────

class TestValidatePositiveNumber:
    def test_valid_int(self):
        assert validate_positive_number(10, "test") is True

    def test_valid_float(self):
        assert validate_positive_number(0.5, "test") is True

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            validate_positive_number(0, "test")

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_positive_number(-1, "test")

    def test_string_raises(self):
        with pytest.raises(TypeError):
            validate_positive_number("abc", "test")


# ── validate_non_negative_number ─────────────────────────────────────

class TestValidateNonNegativeNumber:
    def test_positive(self):
        assert validate_non_negative_number(5, "test") is True

    def test_zero(self):
        assert validate_non_negative_number(0, "test") is True

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_non_negative_number(-1, "test")

    def test_string_raises(self):
        with pytest.raises(TypeError):
            validate_non_negative_number("abc", "test")


# ── load_config ──────────────────────────────────────────────────────

class TestLoadConfig:
    def test_loads_successfully(self):
        config = load_config()
        assert 'cse_fees' in config
        assert 'taxes' in config
        assert 'thresholds' in config

    def test_has_tier_structure(self):
        config = load_config()
        assert 'tier_1' in config['cse_fees']
        assert 'tier_2' in config['cse_fees']

    def test_fee_rates_are_numbers(self):
        config = load_config()
        assert isinstance(config['cse_fees']['tier_1']['broker_commission'], float)


# ── get_data_dir ─────────────────────────────────────────────────────

class TestGetDataDir:
    def test_returns_path(self):
        data_dir = get_data_dir()
        assert data_dir.exists()
        assert data_dir.name == 'data'
