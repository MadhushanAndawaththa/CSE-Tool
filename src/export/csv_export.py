"""
CSV/Excel Export for CSE Stock Analyzer.
"""

import pandas as pd
import os
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


def flatten_result(result):
    """
    Flatten the nested result dictionary for CSV export.
    
    Args:
        result (dict): Complete analysis result
    
    Returns:
        dict: Flattened dictionary
    """
    flat = {}
    
    # Basic Info
    info = result.get('stock_info', {})
    flat['Ticker'] = info.get('ticker', '')
    flat['Company'] = info.get('company_name', '')
    flat['Price'] = info.get('current_price', 0)
    flat['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Overall
    flat['Overall Score'] = result.get('overall_score', 0)
    flat['Recommendation'] = result.get('recommendation', 'N/A')
    flat['Confidence'] = result.get('confidence', 'N/A')
    
    # Fundamental
    fund = result.get('fundamental_analysis', {})
    if fund:
        flat['Fundamental Score'] = fund.get('overall_score', 0)
        metrics = fund.get('metrics', {})
        for k, v in metrics.items():
            if isinstance(v, dict) and k in v:
                flat[f"Fund_{k}"] = v[k]
                
    # Technical
    tech = result.get('technical_analysis', {})
    if tech:
        flat['Technical Score'] = tech.get('overall_score', 0)
        flat['Technical Signal'] = tech.get('overall_signal', 'N/A')
        
        indicators = tech.get('indicators', {})
        if 'rsi' in indicators:
            flat['RSI'] = indicators['rsi'].get('rsi')
        if 'macd' in indicators:
            flat['MACD'] = indicators['macd'].get('signal')
            
    # Risk
    risk = result.get('risk_assessment', {})
    if risk:
        flat['Risk Score'] = risk.get('risk_score', 0)
        flat['Risk Level'] = risk.get('risk_level', 'N/A')
        
    return flat


def export_to_csv(result, filepath):
    """
    Export analysis result to CSV file.
    
    Args:
        result (dict): Complete analysis result
        filepath (str): Output path
    """
    logger.info(f"Exporting results to CSV: {filepath}")
    flat = flatten_result(result)
    df = pd.DataFrame([flat])
    df.to_csv(filepath, index=False)
    logger.info("CSV export successful")
    return filepath


def export_to_excel(result, filepath):
    """
    Export analysis result to Excel file with multiple sheets.
    
    Args:
        result (dict): Complete analysis result
        filepath (str): Output path
    """
    logger.info(f"Exporting results to Excel: {filepath}")
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Summary Sheet
        flat = flatten_result(result)
        pd.DataFrame([flat]).to_excel(writer, sheet_name='Summary', index=False)
        
        # Fundamental Details
        fund = result.get('fundamental_analysis', {})
        if fund and 'metrics' in fund:
            fund_data = []
            for metric, data in fund['metrics'].items():
                if isinstance(data, dict):
                    row = {'Metric': metric}
                    row.update(data)
                    fund_data.append(row)
            if fund_data:
                pd.DataFrame(fund_data).to_excel(writer, sheet_name='Fundamental', index=False)
                
        # Technical Details
        tech = result.get('technical_analysis', {})
        if tech and 'indicators' in tech:
            tech_data = []
            for ind, data in tech['indicators'].items():
                if isinstance(data, dict):
                    # Flatten specific indicators if needed, simplified here
                    row = {'Indicator': ind}
                    # Convert complex values to string
                    clean_data = {k: str(v) if isinstance(v, (dict, list)) else v for k, v in data.items()}
                    row.update(clean_data)
                    tech_data.append(row)
            if tech_data:
                pd.DataFrame(tech_data).to_excel(writer, sheet_name='Technical', index=False)
    
    return filepath
