"""Tests for src.calculations.fundamental module."""

import pytest
from src.calculations.fundamental import FundamentalAnalyzer


class TestFundamentalAnalyzer:
    """Tests for FundamentalAnalyzer class."""

    @pytest.fixture(autouse=True)
    def setup(self, sample_config):
        self.analyzer = FundamentalAnalyzer(custom_config=sample_config)

    # ── P/E Ratio ───────────────────────────────────────────

    def test_pe_ratio_undervalued(self):
        result = self.analyzer.calculate_pe_ratio(100, 10)  # PE = 10
        assert result['pe_ratio'] == 10.0
        assert result['score'] > 50  # Should score well

    def test_pe_ratio_overvalued(self):
        result = self.analyzer.calculate_pe_ratio(500, 10)  # PE = 50
        assert result['pe_ratio'] == 50.0
        assert result['score'] < 50  # Should score poorly

    def test_pe_ratio_zero_eps(self):
        result = self.analyzer.calculate_pe_ratio(100, 0)
        assert result['pe_ratio'] is None or result['score'] == 0

    def test_pe_ratio_negative_eps(self):
        result = self.analyzer.calculate_pe_ratio(100, -5)
        assert result['score'] == 0  # Negative EPS = worst score

    # ── P/B Ratio ───────────────────────────────────────────

    def test_pb_ratio_undervalued(self):
        result = self.analyzer.calculate_pb_ratio(80, 100)  # PB = 0.8
        assert result['pb_ratio'] == 0.8
        assert result['score'] > 50

    def test_pb_ratio_overvalued(self):
        result = self.analyzer.calculate_pb_ratio(400, 100)  # PB = 4.0
        assert result['pb_ratio'] == 4.0
        assert result['score'] < 50

    # ── ROE ──────────────────────────────────────────────────

    def test_roe_excellent(self):
        result = self.analyzer.calculate_roe(25_000, 100_000)  # 25%
        assert result['roe_percentage'] == pytest.approx(25.0)
        assert result['score'] > 70

    def test_roe_poor(self):
        result = self.analyzer.calculate_roe(2_000, 100_000)  # 2%
        assert result['roe_percentage'] == pytest.approx(2.0)
        assert result['score'] < 40

    def test_roe_negative(self):
        result = self.analyzer.calculate_roe(-5_000, 100_000)
        assert result['score'] == 0

    # ── Debt-to-Equity ──────────────────────────────────────

    def test_debt_to_equity_conservative(self):
        result = self.analyzer.calculate_debt_to_equity(30_000, 100_000)  # 0.3
        assert result['debt_to_equity_ratio'] == pytest.approx(0.3)
        assert result['score'] > 70

    def test_debt_to_equity_risky(self):
        result = self.analyzer.calculate_debt_to_equity(300_000, 100_000)  # 3.0
        assert result['debt_to_equity_ratio'] == pytest.approx(3.0)
        assert result['score'] < 30

    # ── Current Ratio ───────────────────────────────────────

    def test_current_ratio_strong(self):
        result = self.analyzer.calculate_current_ratio(200_000, 80_000)  # 2.5
        assert result['current_ratio'] == pytest.approx(2.5)
        assert result['score'] > 70

    def test_current_ratio_concerning(self):
        result = self.analyzer.calculate_current_ratio(80_000, 100_000)  # 0.8
        assert result['current_ratio'] == pytest.approx(0.8)
        assert result['score'] < 40

    # ── Earnings Growth ─────────────────────────────────────

    def test_earnings_growth_positive(self):
        result = self.analyzer.calculate_earnings_growth(15, 10)  # 50%
        assert result['growth_percentage'] == pytest.approx(50.0)
        assert result['score'] > 70

    def test_earnings_growth_negative(self):
        result = self.analyzer.calculate_earnings_growth(8, 10)  # -20%
        assert result['growth_percentage'] == pytest.approx(-20.0)
        assert result['score'] < 30

    # ── Dividend Yield ──────────────────────────────────────

    def test_dividend_yield_basic(self):
        result = self.analyzer.calculate_dividend_yield(5, 100)  # 5%
        assert result['yield_percentage'] == pytest.approx(5.0)
        assert result['score'] > 50

    def test_dividend_yield_zero(self):
        result = self.analyzer.calculate_dividend_yield(0, 100)
        assert result['yield_percentage'] == pytest.approx(0.0)

    # ── Comprehensive analysis ──────────────────────────────

    def test_comprehensive_analysis(self, sample_stock_data):
        result = self.analyzer.comprehensive_analysis(sample_stock_data)
        assert 'overall_score' in result
        assert 'metrics' in result
        assert 'overall_recommendation' in result
        assert 0 <= result['overall_score'] <= 100

    def test_comprehensive_analysis_has_metrics(self, sample_stock_data):
        result = self.analyzer.comprehensive_analysis(sample_stock_data)
        assert 'pe_ratio' in result['metrics']
        assert 'pb_ratio' in result['metrics']
        assert 'roe' in result['metrics']

    def test_comprehensive_analysis_optional_fields(self, sample_stock_data):
        """Test with optional fields like earnings growth and dividend."""
        data = sample_stock_data.copy()
        data['previous_eps'] = 10.00
        data['annual_dividend'] = 3.00
        result = self.analyzer.comprehensive_analysis(data)
        assert result['metrics_analyzed'] > 5  # More metrics with optional data
