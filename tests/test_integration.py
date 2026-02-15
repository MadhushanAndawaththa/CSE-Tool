"""
Integration test: full end-to-end analysis pipeline.

Runs RecommendationEngine.generate_recommendation() with realistic data
and validates the complete output structure.
"""

import pytest

from src.analysis.recommendations import RecommendationEngine


class TestIntegrationFullAnalysis:
    """End-to-end test of the complete analysis pipeline."""

    @pytest.fixture
    def engine(self, sample_config):
        return RecommendationEngine(custom_config=sample_config)

    def test_full_recommendation_with_prices(self, engine, sample_stock_data, sample_prices):
        """Complete recommendation with both fundamental and technical data."""
        result = engine.generate_recommendation(sample_stock_data, prices=sample_prices)

        # ── Structure checks ──────────────────────────────────────
        assert "stock_info" in result
        assert "fundamental_analysis" in result
        assert "technical_analysis" in result
        assert "risk_assessment" in result
        assert "overall_score" in result
        assert "recommendation" in result
        assert "confidence" in result
        assert "key_strengths" in result
        assert "key_concerns" in result
        assert "action_items" in result

        # ── Value range checks ────────────────────────────────────
        assert 0 <= result["overall_score"] <= 100
        assert result["recommendation"] in (
            "STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL", "N/A"
        )
        assert result["confidence"] in ("HIGH", "MODERATE", "MEDIUM", "LOW", "N/A")

        # ── Fundamental sub-result ────────────────────────────────
        fund = result["fundamental_analysis"]
        assert fund is not None
        assert "overall_score" in fund
        assert 0 <= fund["overall_score"] <= 100

        # ── Technical sub-result ──────────────────────────────────
        tech = result["technical_analysis"]
        assert tech is not None
        assert "overall_score" in tech

        # ── Risk sub-result ───────────────────────────────────────
        risk = result["risk_assessment"]
        assert risk is not None
        assert "risk_score" in risk
        assert "risk_level" in risk

    def test_full_recommendation_fundamental_only(self, engine, sample_stock_data):
        """Recommendation with fundamental data only (no prices)."""
        result = engine.generate_recommendation(sample_stock_data)

        assert result["fundamental_analysis"] is not None
        # Technical may be None or have limited data
        assert "overall_score" in result
        assert 0 <= result["overall_score"] <= 100
        assert result["recommendation"] != "N/A"

    def test_full_recommendation_stores_stock_info(self, engine, sample_stock_data, sample_prices):
        """Stock info is correctly propagated to the result."""
        result = engine.generate_recommendation(sample_stock_data, prices=sample_prices)

        info = result["stock_info"]
        assert info.get("ticker") == "JKH"
        assert info.get("company_name") == "John Keells Holdings"
        assert info.get("current_price") == 161.25

    def test_recommendation_with_edge_case_low_eps(self, engine, sample_prices):
        """Stock with negative EPS should still produce a valid result."""
        data = {
            "ticker": "LOSS",
            "company_name": "Loss Corp",
            "price": 50.0,
            "eps": -2.0,
            "book_value_per_share": 30.0,
            "net_income": -500_000_000,
            "shareholders_equity": 5_000_000_000,
            "total_debt": 3_000_000_000,
            "current_assets": 2_000_000_000,
            "current_liabilities": 1_500_000_000,
        }
        result = engine.generate_recommendation(data, prices=sample_prices)
        assert "overall_score" in result
        assert "recommendation" in result

    def test_recommendation_with_minimal_prices(self, engine, sample_stock_data):
        """Very few prices should still return a result (technical may be limited)."""
        short_prices = [100.0, 102.0, 101.5, 103.0, 104.0]
        result = engine.generate_recommendation(sample_stock_data, prices=short_prices)
        assert "overall_score" in result

    def test_different_stocks_get_different_scores(self, engine, sample_prices):
        """Two stocks with different fundamentals should get different scores."""
        strong_stock = {
            "ticker": "STR", "price": 100.0, "eps": 20.0,
            "book_value_per_share": 120.0, "net_income": 10e9,
            "shareholders_equity": 30e9, "total_debt": 5e9,
            "current_assets": 20e9, "current_liabilities": 5e9,
        }
        weak_stock = {
            "ticker": "WK", "price": 100.0, "eps": 2.0,
            "book_value_per_share": 20.0, "net_income": 500e6,
            "shareholders_equity": 5e9, "total_debt": 15e9,
            "current_assets": 3e9, "current_liabilities": 8e9,
        }
        r1 = engine.generate_recommendation(strong_stock, prices=sample_prices)
        r2 = engine.generate_recommendation(weak_stock, prices=sample_prices)
        assert r1["overall_score"] != r2["overall_score"]
