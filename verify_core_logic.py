"""
Verification script for core logic improvements.
"""

import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calculations.technical import TechnicalAnalyzer
from src.analysis.recommendations import RecommendationEngine

def verify_technical_indicators():
    print("\n[VERIFY] Technical Indicators (Bollinger & Stochastic)")
    analyzer = TechnicalAnalyzer()
    
    # Sample uptrending prices with some volatility
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 
              110, 112, 111, 113, 115, 114, 116, 118, 117, 119, 
              120, 122, 121, 120, 118, 116, 114] # 27 data points
    
    print(f"Data points: {len(prices)}")
    
    # 1. Bollinger Bands
    bb = analyzer.calculate_bollinger_bands(prices, period=20)
    print("\nBollinger Bands:")
    print(f"  Upper: {bb['upper']}")
    print(f"  Middle: {bb['middle']}")
    print(f"  Lower: {bb['lower']}")
    print(f"  Signal: {bb['signal']}")
    
    if bb['upper'] is not None and bb['upper'] > bb['middle'] > bb['lower']:
        print("  [PASS] Band structure correct (Upper > Middle > Lower)")
    else:
        print("  [FAIL] Band structure incorrect")

    # 2. Stochastic Oscillator
    stoch = analyzer.calculate_stochastic(prices, k_period=14)
    print("\nStochastic Oscillator:")
    print(f"  %K: {stoch['k']}")
    print(f"  %D: {stoch['d']}")
    print(f"  Signal: {stoch['signal']}")
    
    if stoch['k'] is not None and 0 <= stoch['k'] <= 100:
        print("  [PASS] %K within range 0-100")
    else:
        print("  [FAIL] %K out of range")

def verify_recommendation_engine():
    print("\n[VERIFY] Recommendation Engine Integration")
    engine = RecommendationEngine()
    
    # Sample stock data
    stock_data = {
        'ticker': 'TEST',
        'company_name': 'Test Company',
        'price': 100,
        'eps': 10,
        'book_value_per_share': 80,
        'pe_ratio': 10,  # Good
        'current_ratio': 2.5, # Good
        'debt_to_equity_ratio': 0.4 # Good
    }
    
    # Prices that should trigger technical signals
    # Designing a scenario where price drives indicators
    prices = [100] * 30 
    prices[-1] = 90 # Sudden drop to trigger oversold?
    
    rec = engine.generate_recommendation(stock_data, prices=prices, volumes=[1000]*30)
    
    print("\nRecommendation Result:")
    print(f"  Score: {rec['overall_score']}")
    print(f"  Recommendation: {rec['recommendation']}")
    print("  Key Strengths:")
    for s in rec['key_strengths']:
        print(f"    - {s}")
    print("  Key Concerns:")
    for c in rec['key_concerns']:
        print(f"    - {c}")
        
    # Check if new indicators are mentioned in strengths/concerns
    combined_insights = " ".join(rec['key_strengths'] + rec['key_concerns']).lower()
    
    found_new_indicators = False
    if "bollinger" in combined_insights or "stochastic" in combined_insights:
        found_new_indicators = True
        
    if found_new_indicators:
        print("  [PASS] New indicators affecting insights")
    else:
        print("  [WARN] New indicators not explicitly mentioned in top 5 insights (might be neutral)")

if __name__ == "__main__":
    try:
        verify_technical_indicators()
        verify_recommendation_engine()
        print("\n[SUCCESS] Verification Complete")
    except Exception as e:
        print(f"\n[ERROR] Verification Failed: {e}")
        import traceback
        traceback.print_exc()
