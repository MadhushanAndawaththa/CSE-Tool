"""Tests for src.calculations.technical module."""

import pytest
from src.calculations.technical import TechnicalAnalyzer


class TestTechnicalAnalyzer:
    """Tests for TechnicalAnalyzer class."""

    @pytest.fixture(autouse=True)
    def setup(self, sample_config):
        self.analyzer = TechnicalAnalyzer(custom_config=sample_config)

    # ── RSI ──────────────────────────────────────────────────

    def test_rsi_basic(self, sample_prices):
        result = self.analyzer.calculate_rsi(sample_prices)
        assert result['rsi'] is not None
        assert 0 <= result['rsi'] <= 100

    def test_rsi_has_signal(self, sample_prices):
        result = self.analyzer.calculate_rsi(sample_prices)
        assert 'signal' in result
        assert result['signal'] in ['STRONG BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG SELL']

    def test_rsi_insufficient_data(self):
        result = self.analyzer.calculate_rsi([100, 101, 102])
        assert result['rsi'] is None or result.get('error') is not None

    def test_rsi_uptrend_not_oversold(self, uptrend_prices):
        result = self.analyzer.calculate_rsi(uptrend_prices)
        if result['rsi'] is not None:
            assert result['rsi'] > 30  # Uptrend should not be oversold

    def test_rsi_downtrend_not_overbought(self, downtrend_prices):
        result = self.analyzer.calculate_rsi(downtrend_prices)
        if result['rsi'] is not None:
            assert result['rsi'] < 70  # Downtrend should not be overbought

    # ── MACD ─────────────────────────────────────────────────

    def test_macd_basic(self, sample_prices):
        result = self.analyzer.calculate_macd(sample_prices)
        assert 'macd' in result
        assert 'signal_line' in result
        assert 'histogram' in result

    def test_macd_has_signal(self, sample_prices):
        result = self.analyzer.calculate_macd(sample_prices)
        assert 'signal' in result

    def test_macd_insufficient_data(self):
        result = self.analyzer.calculate_macd([100, 101, 102, 103, 104])
        assert result['macd'] is None or result.get('error') is not None

    # ── Moving Averages ──────────────────────────────────────

    def test_moving_averages_basic(self, sample_prices):
        result = self.analyzer.calculate_moving_averages(sample_prices)
        assert 'short_ma' in result
        assert 'current_price' in result
        assert 'signal' in result

    def test_moving_averages_insufficient_data(self):
        result = self.analyzer.calculate_moving_averages([100, 101, 102])
        assert result['short_ma'] is None

    # ── Bollinger Bands ──────────────────────────────────────

    def test_bollinger_bands_structure(self, sample_prices):
        result = self.analyzer.calculate_bollinger_bands(sample_prices, period=20)
        assert 'upper' in result
        assert 'middle' in result
        assert 'lower' in result

    def test_bollinger_bands_ordering(self, sample_prices):
        result = self.analyzer.calculate_bollinger_bands(sample_prices, period=20)
        if result['upper'] is not None:
            assert result['upper'] > result['middle'] > result['lower']

    def test_bollinger_bands_has_signal(self, sample_prices):
        result = self.analyzer.calculate_bollinger_bands(sample_prices, period=20)
        assert 'signal' in result

    def test_bollinger_bands_insufficient_data(self):
        result = self.analyzer.calculate_bollinger_bands([100, 101, 102], period=20)
        assert result['upper'] is None

    # ── Stochastic Oscillator ────────────────────────────────

    def test_stochastic_basic(self, sample_prices):
        result = self.analyzer.calculate_stochastic(sample_prices)
        assert 'k' in result
        assert 'd' in result

    def test_stochastic_k_range(self, sample_prices):
        result = self.analyzer.calculate_stochastic(sample_prices)
        if result['k'] is not None:
            assert 0 <= result['k'] <= 100

    def test_stochastic_has_signal(self, sample_prices):
        result = self.analyzer.calculate_stochastic(sample_prices)
        assert 'signal' in result

    def test_stochastic_insufficient_data(self):
        result = self.analyzer.calculate_stochastic([100, 101])
        assert result['k'] is None

    # ── Volume Analysis ──────────────────────────────────────

    def test_volume_analysis(self, sample_prices):
        volumes = [1000 + i * 10 for i in range(len(sample_prices))]
        result = self.analyzer.calculate_volume_analysis(sample_prices, volumes)
        assert 'volume_trend' in result

    # ── Comprehensive Analysis ───────────────────────────────

    def test_comprehensive_analysis(self, sample_prices):
        result = self.analyzer.comprehensive_analysis(sample_prices)
        assert 'overall_score' in result
        assert 'overall_signal' in result
        assert 0 <= result['overall_score'] <= 100

    def test_comprehensive_analysis_has_indicators(self, sample_prices):
        result = self.analyzer.comprehensive_analysis(sample_prices)
        assert 'indicators' in result
        assert 'rsi' in result['indicators']
        assert 'macd' in result['indicators']
        assert 'moving_averages' in result['indicators']

    def test_comprehensive_analysis_with_volumes(self, sample_prices):
        volumes = [1000] * len(sample_prices)
        result = self.analyzer.comprehensive_analysis(sample_prices, volumes=volumes)
        assert 'overall_score' in result

    def test_comprehensive_analysis_insufficient_data(self):
        result = self.analyzer.comprehensive_analysis([100, 101, 102])
        assert 'overall_score' in result  # Should still return, possibly with 0 or limited analysis
