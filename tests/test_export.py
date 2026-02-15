
import pytest
import os
from src.export.pdf_report import generate_pdf_report
from src.export.csv_export import export_to_csv, export_to_excel

@pytest.fixture
def sample_analysis_result():
    return {
        'stock_info': {
            'ticker': 'TEST.N0000',
            'company_name': 'Test Company PLC',
            'current_price': 150.0
        },
        'overall_score': 85,
        'recommendation': 'STRONG BUY',
        'confidence': 'High',
        'fundamental_analysis': {
            'overall_score': 80,
            'metrics': {
                'pe_ratio': 10.5,
                'pb_ratio': 1.2
            }
        },
        'technical_analysis': {
            'overall_score': 90,
            'overall_signal': 'BULLISH',
            'indicators': {
                'rsi': {'rsi': 35, 'interpretation': 'Oversold'},
                'macd': {'signal': 'BUY', 'interpretation': 'Bullish crossover'}
            }
        },
        'risk_assessment': {
            'risk_score': 20,
            'risk_level': 'Low Risk',
            'risk_factors': ['Market volatility']
        },
        'key_strengths': ['Good value', 'Strong momentum'],
        'key_concerns': ['Sector headwinds'],
        'action_items': ['Buy at market price']
    }

def test_pdf_generation(sample_analysis_result, tmp_path):
    output_file = tmp_path / "report.pdf"
    generate_pdf_report(sample_analysis_result, str(output_file))
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_csv_export(sample_analysis_result, tmp_path):
    output_file = tmp_path / "export.csv"
    export_to_csv(sample_analysis_result, str(output_file))
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_excel_export(sample_analysis_result, tmp_path):
    output_file = tmp_path / "export.xlsx"
    export_to_excel(sample_analysis_result, str(output_file))
    assert output_file.exists()
    assert output_file.stat().st_size > 0
