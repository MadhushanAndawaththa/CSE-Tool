"""Tests for src.fees.cse_fees module."""

import pytest
from src.fees.cse_fees import CSEFeeCalculator, calculate_buy_fees, calculate_sell_fees


class TestCSEFeeCalculator:
    """Tests for CSEFeeCalculator class."""

    @pytest.fixture(autouse=True)
    def setup(self, sample_config):
        self.calc = CSEFeeCalculator(custom_config=sample_config)

    # ── Tier selection ───────────────────────────────────────

    def test_tier_1_selection(self):
        rates = self.calc._get_fee_rates(1_000_000)
        assert rates['broker_commission'] == 0.00640

    def test_tier_2_selection(self):
        rates = self.calc._get_fee_rates(200_000_000)
        assert rates['broker_commission'] == 0.002000

    def test_tier_boundary(self):
        """Exactly Rs. 100Mn should be Tier 1."""
        rates = self.calc._get_fee_rates(100_000_000)
        assert rates['broker_commission'] == 0.00640

    def test_above_tier_boundary(self):
        rates = self.calc._get_fee_rates(100_000_001)
        assert rates['broker_commission'] == 0.002000

    # ── Buy fees ────────────────────────────────────────────

    def test_buy_fees_basic(self):
        result = self.calc.calculate_buy_fees(100_000)
        assert result['transaction_value'] == 100_000
        assert result['total_cost'] > 100_000
        assert result['total_fees'] > 0

    def test_buy_fees_components(self):
        result = self.calc.calculate_buy_fees(1_000_000)
        assert result['broker_commission'] == 1_000_000 * 0.00640
        assert result['sec_fee'] == 1_000_000 * 0.00072
        assert result['cse_fee'] == 1_000_000 * 0.00084
        assert result['cds_fee'] == 1_000_000 * 0.00024

    def test_buy_fees_minimum_commission(self):
        """Very small transaction should apply minimum commission."""
        result = self.calc.calculate_buy_fees(1_000)
        # 1000 * 0.0064 = 6.4, but minimum is 100
        assert result['broker_commission'] == 100

    def test_buy_fees_total_cost_equals_value_plus_fees(self):
        result = self.calc.calculate_buy_fees(500_000)
        assert abs(result['total_cost'] - (result['transaction_value'] + result['total_fees'])) < 0.01

    def test_buy_fees_no_stl(self):
        """Buy fees should NOT include STL tax."""
        result = self.calc.calculate_buy_fees(1_000_000)
        assert 'stl_tax' not in result

    def test_buy_fees_tier_label(self):
        result = self.calc.calculate_buy_fees(50_000)
        assert 'Tier 1' in result['tier']

    # ── Sell fees ───────────────────────────────────────────

    def test_sell_fees_basic(self):
        result = self.calc.calculate_sell_fees(100_000)
        assert result['net_proceeds'] < 100_000
        assert result['total_fees'] > 0

    def test_sell_fees_includes_stl(self):
        result = self.calc.calculate_sell_fees(1_000_000)
        assert result['stl_tax'] == 1_000_000 * 0.003

    def test_sell_fees_higher_than_buy(self):
        """Sell fees should be higher than buy fees due to STL."""
        buy = self.calc.calculate_buy_fees(1_000_000)
        sell = self.calc.calculate_sell_fees(1_000_000)
        assert sell['total_fees'] > buy['total_fees']

    def test_sell_fees_net_proceeds(self):
        result = self.calc.calculate_sell_fees(1_000_000)
        assert abs(result['net_proceeds'] - (result['transaction_value'] - result['total_fees'])) < 0.01

    # ── Capital gains tax ───────────────────────────────────

    def test_capital_gains_tax_on_profit(self):
        result = self.calc.calculate_capital_gains_tax(100_000)
        assert result['tax_amount'] == 30_000  # 30%
        assert result['net_profit_after_tax'] == 70_000

    def test_capital_gains_tax_on_loss(self):
        result = self.calc.calculate_capital_gains_tax(-50_000)
        assert result['tax_amount'] == 0
        assert result['net_profit_after_tax'] == -50_000

    def test_capital_gains_tax_zero(self):
        result = self.calc.calculate_capital_gains_tax(0)
        assert result['tax_amount'] == 0

    # ── Round trip ──────────────────────────────────────────

    def test_round_trip_profit(self):
        result = self.calc.calculate_round_trip_cost(100, 120, 1000)
        assert result['gross_profit'] > 0
        assert result['net_profit'] < result['gross_profit']  # Tax reduces profit

    def test_round_trip_loss(self):
        result = self.calc.calculate_round_trip_cost(120, 100, 1000)
        assert result['gross_profit'] < 0
        assert result['capital_gains_tax']['tax_amount'] == 0  # No tax on loss

    def test_round_trip_total_fees(self):
        result = self.calc.calculate_round_trip_cost(100, 110, 100)
        buy_fees = result['buy_fees']['total_fees']
        sell_fees = result['sell_fees']['total_fees']
        assert abs(result['total_fees'] - (buy_fees + sell_fees)) < 0.01

    # ── Validation ──────────────────────────────────────────

    def test_buy_fees_invalid_value(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_buy_fees(-1000)

    def test_sell_fees_invalid_value(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_sell_fees(-1000)

    def test_round_trip_invalid_price(self):
        with pytest.raises((ValueError, TypeError)):
            self.calc.calculate_round_trip_cost(-100, 120, 1000)

    # ── Fee summary ─────────────────────────────────────────

    def test_fee_summary_has_all_keys(self):
        summary = self.calc.get_fee_summary()
        expected_keys = [
            'tier_1_brokerage', 'tier_1_cse', 'tier_1_cds', 'tier_1_sec', 'tier_1_stl',
            'tier_2_brokerage', 'tier_2_cse', 'tier_2_cds', 'tier_2_sec', 'tier_2_stl',
            'capital_gains_tax', 'minimum_commission',
        ]
        for key in expected_keys:
            assert key in summary


# ── Convenience functions ────────────────────────────────────────────

class TestConvenienceFunctions:
    def test_calculate_buy_fees(self, sample_config):
        result = calculate_buy_fees(100, 1000, custom_config=sample_config)
        assert result['total_cost'] > 100_000

    def test_calculate_sell_fees(self, sample_config):
        result = calculate_sell_fees(100, 1000, custom_config=sample_config)
        assert result['net_proceeds'] < 100_000
