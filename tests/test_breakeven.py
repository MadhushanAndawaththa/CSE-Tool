"""Tests for src.calculations.breakeven module."""

import pytest
from src.calculations.breakeven import BreakEvenCalculator, calculate_breakeven


class TestBreakEvenCalculator:
    """Tests for BreakEvenCalculator class."""

    @pytest.fixture(autouse=True)
    def setup(self, sample_config):
        self.calc = BreakEvenCalculator(custom_config=sample_config)

    # ── Breakeven price ─────────────────────────────────────

    def test_breakeven_without_tax(self):
        result = self.calc.calculate_breakeven_price(100, 1000, include_tax=False)
        assert result['breakeven_price'] > 100  # Must be above buy price
        assert result['includes_capital_gains_tax'] is False
        assert result['price_increase_required'] > 0

    def test_breakeven_with_tax(self):
        result = self.calc.calculate_breakeven_price(100, 1000, include_tax=True)
        assert result['breakeven_price'] > 100
        assert result['includes_capital_gains_tax'] is True

    def test_breakeven_with_tax_higher_than_without(self):
        with_tax = self.calc.calculate_breakeven_price(100, 1000, include_tax=True)
        without_tax = self.calc.calculate_breakeven_price(100, 1000, include_tax=False)
        assert with_tax['breakeven_price'] >= without_tax['breakeven_price']

    def test_breakeven_percentage_positive(self):
        result = self.calc.calculate_breakeven_price(100, 1000)
        assert result['price_increase_percentage'] > 0

    def test_breakeven_contains_expected_keys(self):
        result = self.calc.calculate_breakeven_price(100, 1000)
        expected = [
            'buy_price', 'quantity', 'total_investment', 'buy_fees_paid',
            'breakeven_price', 'price_increase_required', 'price_increase_percentage',
        ]
        for key in expected:
            assert key in result

    def test_breakeven_investment_greater_than_principal(self):
        result = self.calc.calculate_breakeven_price(100, 1000)
        assert result['total_investment'] > 100 * 1000

    # ── Target price ────────────────────────────────────────

    def test_target_price_10_percent(self):
        result = self.calc.calculate_target_price(100, 1000, 10)
        assert result['target_sell_price'] > result['breakeven_price']
        assert result['target_profit_percentage'] == 10

    def test_target_price_higher_for_larger_target(self):
        result_10 = self.calc.calculate_target_price(100, 1000, 10)
        result_20 = self.calc.calculate_target_price(100, 1000, 20)
        assert result_20['target_sell_price'] > result_10['target_sell_price']

    def test_target_price_without_tax(self):
        result = self.calc.calculate_target_price(100, 1000, 15, include_tax=False)
        assert result['includes_capital_gains_tax'] is False
        assert result['capital_gains_tax'] == 0

    def test_target_price_contains_expected_keys(self):
        result = self.calc.calculate_target_price(100, 1000, 15)
        expected = [
            'buy_price', 'quantity', 'total_investment', 'target_sell_price',
            'breakeven_price', 'net_profit', 'actual_profit_percentage',
        ]
        for key in expected:
            assert key in result

    # ── Profit at price ─────────────────────────────────────

    def test_profit_at_higher_price(self):
        result = self.calc.calculate_profit_at_price(100, 120, 1000)
        assert result['net_profit'] > 0
        assert result['above_breakeven'] is True

    def test_loss_at_lower_price(self):
        result = self.calc.calculate_profit_at_price(100, 90, 1000)
        assert result['net_profit'] < 0
        assert result['above_breakeven'] is False

    def test_profit_at_price_percentage(self):
        result = self.calc.calculate_profit_at_price(100, 120, 1000)
        assert result['profit_percentage'] > 0

    def test_loss_at_price_no_tax(self):
        result = self.calc.calculate_profit_at_price(100, 80, 1000)
        assert result['capital_gains_tax'] == 0  # No tax on loss

    def test_profit_at_price_contains_expected_keys(self):
        result = self.calc.calculate_profit_at_price(100, 120, 1000)
        expected = [
            'buy_price', 'sell_price', 'quantity', 'total_investment',
            'total_fees', 'gross_profit', 'net_profit', 'profit_percentage',
            'breakeven_price', 'above_breakeven',
        ]
        for key in expected:
            assert key in result

    # ── Validation ──────────────────────────────────────────

    def test_invalid_buy_price(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_breakeven_price(-100, 1000)

    def test_invalid_quantity(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_breakeven_price(100, -1000)

    def test_invalid_target_percentage(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_target_price(100, 1000, -10)


# ── Convenience function ─────────────────────────────────────────────

class TestConvenienceFunction:
    def test_calculate_breakeven(self, sample_config):
        result = calculate_breakeven(100, 1000, custom_config=sample_config)
        assert result['breakeven_price'] > 100
