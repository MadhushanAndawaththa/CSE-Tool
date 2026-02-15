"""
Tests for the SQLite AnalysisDatabase storage layer.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path

from src.storage.database import AnalysisDatabase


@pytest.fixture
def tmp_db(tmp_path):
    """Create a temporary database for testing."""
    db = AnalysisDatabase(db_dir=str(tmp_path), db_name="test.db")
    yield db
    # cleanup handled by tmp_path


@pytest.fixture
def sample_result():
    """Minimal analysis result dict for save/load tests."""
    return {
        "stock_info": {
            "ticker": "JKH",
            "company_name": "John Keells Holdings",
            "current_price": 161.25,
        },
        "overall_score": 72.5,
        "recommendation": "BUY",
        "confidence": "HIGH",
        "fundamental_analysis": {"overall_score": 75},
        "technical_analysis": {"overall_score": 68},
        "risk_assessment": {"risk_score": 70, "risk_level": "MODERATE RISK"},
        "key_strengths": ["Strong ROE"],
        "key_concerns": ["High debt"],
        "action_items": ["Monitor quarterly earnings"],
    }


class TestAnalysisDatabase:
    """Tests for AnalysisDatabase CRUD operations."""

    def test_save_and_retrieve(self, tmp_db, sample_result):
        """Round-trip: save then retrieve by ID."""
        row_id = tmp_db.save_analysis(sample_result)
        assert row_id > 0

        loaded = tmp_db.get_analysis_by_id(row_id)
        assert loaded is not None
        assert loaded["stock_info"]["ticker"] == "JKH"
        assert loaded["overall_score"] == 72.5
        assert loaded["recommendation"] == "BUY"

    def test_get_history(self, tmp_db, sample_result):
        """History returns latest first, respects limit."""
        ids = []
        for i in range(5):
            result = {**sample_result}
            result["stock_info"] = {**sample_result["stock_info"], "ticker": f"T{i}"}
            result["overall_score"] = 50 + i * 5
            ids.append(tmp_db.save_analysis(result))

        history = tmp_db.get_history(limit=3)
        assert len(history) == 3
        # Latest first
        assert history[0]["ticker"] == "T4"
        assert history[2]["ticker"] == "T2"

    def test_get_history_empty(self, tmp_db):
        """Empty database returns empty list."""
        assert tmp_db.get_history() == []

    def test_get_analysis_not_found(self, tmp_db):
        """Non-existent ID returns None."""
        assert tmp_db.get_analysis_by_id(999) is None

    def test_save_minimal_result(self, tmp_db):
        """Save result missing optional fields."""
        minimal = {"overall_score": 50, "recommendation": "HOLD"}
        row_id = tmp_db.save_analysis(minimal)
        assert row_id > 0

        loaded = tmp_db.get_analysis_by_id(row_id)
        assert loaded is not None
        assert loaded["recommendation"] == "HOLD"

    def test_multiple_saves_increment_id(self, tmp_db, sample_result):
        """Each save gets a unique incrementing ID."""
        id1 = tmp_db.save_analysis(sample_result)
        id2 = tmp_db.save_analysis(sample_result)
        assert id2 > id1

    def test_db_file_created(self, tmp_path):
        """Database file is created on disk."""
        db = AnalysisDatabase(db_dir=str(tmp_path), db_name="check.db")
        assert (tmp_path / "check.db").exists()

    def test_history_fields(self, tmp_db, sample_result):
        """History records contain expected summary fields."""
        tmp_db.save_analysis(sample_result)
        history = tmp_db.get_history()
        assert len(history) == 1
        record = history[0]
        assert "ticker" in record
        assert "overall_score" in record
        assert "recommendation" in record
        assert "timestamp" in record
