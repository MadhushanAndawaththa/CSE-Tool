"""
SQLite Database Storage for CSE Stock Analyzer.

Handles persistence of analysis results and retrieval of history.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

DB_DIR = "data"
DB_NAME = "cse_analyzer.db"

class AnalysisDatabase:
    """Manages SQLite database for storing analysis results."""
    
    def __init__(self, db_dir: str = DB_DIR, db_name: str = DB_NAME):
        """
        Initialize database connection.
        
        Args:
            db_dir: Directory to store database file
            db_name: Name of the database file
        """
        db_path = Path(db_dir)
        db_path.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path / db_name
            
        self._init_db()
        
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        return sqlite3.connect(self.db_path)
        
    def _init_db(self) -> None:
        """Initialize database schema."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Create history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analysis_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        ticker TEXT,
                        company_name TEXT,
                        current_price REAL,
                        overall_score REAL,
                        recommendation TEXT,
                        confidence TEXT,
                        full_result JSON
                    )
                """)
                
                conn.commit()
                logger.debug("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise

    def save_analysis(self, result: Dict[str, Any]) -> int:
        """
        Save an analysis result to the database.
        
        Args:
            result: Complete analysis result dictionary
            
        Returns:
            int: ID of the inserted record
        """
        try:
            # Extract high-level fields
            timestamp = datetime.now().isoformat()
            stock_info = result.get('stock_info', {})
            
            ticker = stock_info.get('ticker')
            company = stock_info.get('company_name')
            price = stock_info.get('current_price')
            
            score = result.get('overall_score')
            rec = result.get('recommendation')
            conf = result.get('confidence')
            
            # Serialize full result
            full_result_json = json.dumps(result)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO analysis_history 
                    (timestamp, ticker, company_name, current_price, overall_score, recommendation, confidence, full_result)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, ticker, company, price, score, rec, conf, full_result_json))
                
                row_id = cursor.lastrowid
                conn.commit()
                
            logger.info(f"Analysis saved for {ticker} with ID {row_id}")
            return row_id
            
        except Exception as e:
            logger.error(f"Failed to save analysis: {str(e)}")
            return -1

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve analysis history (summaries).
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List[Dict]: List of history records (latest first)
        """
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, timestamp, ticker, company_name, current_price, overall_score, recommendation, confidence
                    FROM analysis_history
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                
                # Convert to list of dicts
                history = [dict(row) for row in rows]
                
            return history
            
        except Exception as e:
            logger.error(f"Failed to retrieve history: {str(e)}")
            return []

    def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve full analysis result by ID.
        
        Args:
            analysis_id: ID of the record
            
        Returns:
            Optional[Dict]: Full analysis result or None if not found
        """
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT full_result FROM analysis_history WHERE id = ?
                """, (analysis_id,))
                
                row = cursor.fetchone()
                
                if row:
                    return json.loads(row['full_result'])
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve analysis details: {str(e)}")
            return None
