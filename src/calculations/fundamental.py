"""
Fundamental Analysis Module for Stock Valuation.

This module calculates key fundamental analysis ratios used by professional
investors to evaluate stock value, including P/E ratio, P/B ratio, ROE,
debt-to-equity ratio, and other financial metrics.
"""

from src.utils.helpers import load_config, validate_positive_number, validate_non_negative_number
from typing import Any, Dict, Optional


class FundamentalAnalyzer:
    """Calculate and analyze fundamental stock metrics."""
    
    def __init__(self, custom_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize fundamental analyzer.
        
        Args:
            custom_config: Optional dictionary to override default config
        """
        self.config = custom_config if custom_config else load_config()
        self.thresholds = self.config['thresholds']
    
    def calculate_pe_ratio(self, price: float, eps: float) -> Dict[str, Any]:
        """
        Calculate Price-to-Earnings (P/E) ratio.
        
        P/E Ratio = Market Price per Share / Earnings per Share
        
        Args:
            price: Current market price per share
            eps: Earnings per share (annual)
        
        Returns:
            dict: P/E ratio and interpretation
        """
        validate_positive_number(price, "Price")
        
        if eps <= 0:
            return {
                'pe_ratio': None,
                'score': 0,
                'interpretation': 'Negative or zero earnings',
                'recommendation': 'AVOID - Company is not profitable',
                'rating': 'Poor'
            }
        
        pe_ratio = price / eps
        
        # Score based on thresholds
        pe_thresholds = self.thresholds['pe_ratio']
        if pe_ratio < pe_thresholds['undervalued']:
            score = 100
            interpretation = 'Significantly undervalued'
            recommendation = 'STRONG BUY'
        elif pe_ratio < pe_thresholds['fair_value_min']:
            score = 85
            interpretation = 'Undervalued'
            recommendation = 'BUY'
        elif pe_ratio <= pe_thresholds['fair_value_max']:
            score = 70
            interpretation = 'Fairly valued'
            recommendation = 'HOLD'
        elif pe_ratio <= pe_thresholds['overvalued']:
            score = 50
            interpretation = 'Slightly overvalued'
            recommendation = 'HOLD/SELL'
        else:
            score = 25
            interpretation = 'Overvalued'
            recommendation = 'SELL'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'STRONG BUY': 'Excellent',
            'BUY': 'Good',
            'HOLD': 'Fair',
            'HOLD/SELL': 'Fair',
            'SELL': 'Poor',
            'AVOID - Company is not profitable': 'Poor'
        }
        
        return {
            'pe_ratio': round(pe_ratio, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair'),
            'benchmark_range': f"{pe_thresholds['fair_value_min']}-{pe_thresholds['fair_value_max']}"
        }
    
    def calculate_pb_ratio(self, price: float, book_value_per_share: float) -> Dict[str, Any]:
        """
        Calculate Price-to-Book (P/B) ratio.
        
        P/B Ratio = Market Price per Share / Book Value per Share
        
        Args:
            price: Current market price per share
            book_value_per_share: Book value (net assets) per share
        
        Returns:
            dict: P/B ratio and interpretation
        """
        validate_positive_number(price, "Price")
        validate_positive_number(book_value_per_share, "Book value per share")
        
        pb_ratio = price / book_value_per_share
        
        # Score based on thresholds
        pb_thresholds = self.thresholds['pb_ratio']
        if pb_ratio < pb_thresholds['undervalued']:
            score = 100
            interpretation = 'Trading below book value - potential value opportunity'
            recommendation = 'STRONG BUY'
        elif pb_ratio <= pb_thresholds['fair_value']:
            score = 80
            interpretation = 'Reasonably valued relative to assets'
            recommendation = 'BUY'
        elif pb_ratio <= pb_thresholds['overvalued']:
            score = 60
            interpretation = 'Moderate premium to book value'
            recommendation = 'HOLD'
        else:
            score = 35
            interpretation = 'High premium to book value'
            recommendation = 'SELL'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'STRONG BUY': 'Excellent',
            'BUY': 'Good',
            'HOLD': 'Fair',
            'SELL': 'Poor'
        }
        
        return {
            'pb_ratio': round(pb_ratio, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def calculate_roe(self, net_income: float, shareholders_equity: float) -> Dict[str, Any]:
        """
        Calculate Return on Equity (ROE).
        
        ROE = Net Income / Shareholders' Equity
        
        Args:
            net_income: Annual net income
            shareholders_equity: Total shareholders' equity
        
        Returns:
            dict: ROE and interpretation
        """
        # Handle negative equity (distressed companies)
        if shareholders_equity <= 0:
            return {
                'roe': 0,
                'roe_percentage': 0,
                'score': 0,
                'interpretation': 'Negative or zero shareholders equity - company is insolvent',
                'recommendation': 'AVOID - Company has negative equity',
                'rating': 'Poor'
            }
        
        validate_positive_number(shareholders_equity, "Shareholders' equity")
        
        if net_income <= 0:
            return {
                'roe': 0,
                'roe_percentage': 0,
                'score': 0,
                'interpretation': 'Negative or zero net income',
                'recommendation': 'POOR - Company not generating profit for shareholders',
                'rating': 'Poor'
            }
        
        roe = net_income / shareholders_equity
        roe_percentage = roe * 100
        
        # Score based on thresholds
        roe_thresholds = self.thresholds['roe']
        if roe >= roe_thresholds['excellent']:
            score = 100
            interpretation = 'Excellent returns on shareholder capital'
            recommendation = 'STRONG BUY'
        elif roe >= roe_thresholds['good']:
            score = 85
            interpretation = 'Good profitability'
            recommendation = 'BUY'
        elif roe >= roe_thresholds['acceptable']:
            score = 65
            interpretation = 'Acceptable returns'
            recommendation = 'HOLD'
        elif roe >= roe_thresholds['poor']:
            score = 40
            interpretation = 'Below average returns'
            recommendation = 'HOLD/SELL'
        else:
            score = 20
            interpretation = 'Poor returns on equity'
            recommendation = 'SELL'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'STRONG BUY': 'Excellent',
            'BUY': 'Good',
            'HOLD': 'Fair',
            'HOLD/SELL': 'Fair',
            'SELL': 'Poor',
            'POOR - Company not generating profit for shareholders': 'Poor'
        }
        
        return {
            'roe': round(roe, 4),
            'roe_percentage': round(roe_percentage, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def calculate_debt_to_equity(self, total_debt: float, shareholders_equity: float) -> Dict[str, Any]:
        """
        Calculate Debt-to-Equity ratio.
        
        D/E Ratio = Total Debt / Shareholders' Equity
        
        Args:
            total_debt: Total liabilities/debt
            shareholders_equity: Total shareholders' equity
        
        Returns:
            dict: D/E ratio and interpretation
        """
        validate_non_negative_number(total_debt, "Total debt")
        validate_positive_number(shareholders_equity, "Shareholders' equity")
        
        de_ratio = total_debt / shareholders_equity
        
        # Score based on thresholds (lower is better for risk)
        de_thresholds = self.thresholds['debt_to_equity']
        if de_ratio <= de_thresholds['conservative']:
            score = 100
            interpretation = 'Very conservative leverage - low financial risk'
            recommendation = 'EXCELLENT - Strong balance sheet'
        elif de_ratio <= de_thresholds['moderate']:
            score = 80
            interpretation = 'Moderate leverage - manageable debt levels'
            recommendation = 'GOOD - Balanced capital structure'
        elif de_ratio <= de_thresholds['aggressive']:
            score = 55
            interpretation = 'Elevated leverage - monitor debt levels'
            recommendation = 'CAUTION - Higher financial risk'
        elif de_ratio <= de_thresholds['risky']:
            score = 30
            interpretation = 'High leverage - significant financial risk'
            recommendation = 'RISKY - Vulnerable to economic downturns'
        else:
            score = 10
            interpretation = 'Very high leverage - potential solvency concerns'
            recommendation = 'HIGH RISK - Avoid unless restructuring'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'EXCELLENT - Strong balance sheet': 'Excellent',
            'GOOD - Balanced capital structure': 'Good',
            'CAUTION - Higher financial risk': 'Fair',
            'RISKY - Vulnerable to economic downturns': 'Poor',
            'HIGH RISK - Avoid unless restructuring': 'Poor'
        }
        
        return {
            'debt_to_equity_ratio': round(de_ratio, 2),
            'debt_to_equity': round(de_ratio, 2),  # Add alias for GUI
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def calculate_current_ratio(self, current_assets, current_liabilities):
        """
        Calculate Current Ratio (liquidity measure).
        
        Current Ratio = Current Assets / Current Liabilities
        
        Args:
            current_assets: Total current assets
            current_liabilities: Total current liabilities
        
        Returns:
            dict: Current ratio and interpretation
        """
        validate_positive_number(current_assets, "Current assets")
        validate_positive_number(current_liabilities, "Current liabilities")
        
        current_ratio = current_assets / current_liabilities
        
        # Score based on thresholds
        cr_thresholds = self.thresholds['current_ratio']
        if current_ratio >= cr_thresholds['strong']:
            score = 100
            interpretation = 'Strong liquidity - can easily cover short-term obligations'
            recommendation = 'EXCELLENT'
        elif current_ratio >= cr_thresholds['adequate']:
            score = 80
            interpretation = 'Adequate liquidity position'
            recommendation = 'GOOD'
        elif current_ratio >= cr_thresholds['concerning']:
            score = 50
            interpretation = 'Marginal liquidity - monitor cash flow'
            recommendation = 'CAUTION'
        else:
            score = 20
            interpretation = 'Liquidity concerns - may struggle with short-term obligations'
            recommendation = 'RISK - Potential solvency issues'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'EXCELLENT': 'Excellent',
            'GOOD': 'Good',
            'CAUTION': 'Fair',
            'RISK - Potential solvency issues': 'Poor'
        }
        
        return {
            'current_ratio': round(current_ratio, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def calculate_earnings_growth(self, current_eps, previous_eps):
        """
        Calculate Earnings Growth Rate.
        
        Growth Rate = (Current EPS - Previous EPS) / Previous EPS
        
        Args:
            current_eps: Current year earnings per share
            previous_eps: Previous year earnings per share
        
        Returns:
            dict: Earnings growth rate and interpretation
        """
        if previous_eps <= 0:
            return {
                'earnings_growth': None,
                'growth_percentage': None,
                'score': 0,
                'interpretation': 'Cannot calculate - previous year had no earnings',
                'recommendation': 'N/A',
                'rating': 'Poor'
            }
        
        growth_rate = (current_eps - previous_eps) / previous_eps
        growth_percentage = growth_rate * 100
        
        # Score based on thresholds
        eg_thresholds = self.thresholds['earnings_growth']
        if growth_rate >= eg_thresholds['excellent']:
            score = 100
            interpretation = 'Excellent growth - strong business momentum'
            recommendation = 'STRONG BUY'
        elif growth_rate >= eg_thresholds['good']:
            score = 85
            interpretation = 'Good growth trajectory'
            recommendation = 'BUY'
        elif growth_rate >= eg_thresholds['moderate']:
            score = 70
            interpretation = 'Moderate growth'
            recommendation = 'HOLD'
        elif growth_rate >= 0:
            score = 55
            interpretation = 'Slow growth'
            recommendation = 'HOLD'
        else:
            score = 25
            interpretation = 'Declining earnings - negative growth'
            recommendation = 'SELL'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'STRONG BUY': 'Excellent',
            'BUY': 'Good',
            'HOLD': 'Fair',
            'SELL': 'Poor'
        }
        
        return {
            'earnings_growth': round(growth_rate, 4),
            'growth_percentage': round(growth_percentage, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def calculate_dividend_yield(self, annual_dividend, price):
        """
        Calculate Dividend Yield.
        
        Dividend Yield = Annual Dividend per Share / Price per Share
        
        Args:
            annual_dividend: Annual dividend per share
            price: Current market price per share
        
        Returns:
            dict: Dividend yield and interpretation
        """
        validate_non_negative_number(annual_dividend, "Annual dividend")
        validate_positive_number(price, "Price")
        
        if annual_dividend == 0:
            return {
                'dividend_yield': 0,
                'yield_percentage': 0,
                'score': 50,
                'interpretation': 'No dividend - growth stock or retaining earnings',
                'recommendation': 'Neutral - evaluate based on growth potential',
                'rating': 'Fair'
            }
        
        dividend_yield = annual_dividend / price
        yield_percentage = dividend_yield * 100
        
        # Score based on yield (higher is better for income investors)
        if yield_percentage >= 5.0:
            score = 90
            interpretation = 'High dividend yield - good income generation'
            recommendation = 'ATTRACTIVE for income investors'
        elif yield_percentage >= 3.0:
            score = 80
            interpretation = 'Good dividend yield'
            recommendation = 'GOOD for balanced portfolios'
        elif yield_percentage >= 1.5:
            score = 65
            interpretation = 'Moderate dividend yield'
            recommendation = 'ACCEPTABLE'
        else:
            score = 50
            interpretation = 'Low dividend yield'
            recommendation = 'Evaluate for growth potential instead'
        
        # Map recommendation to rating for GUI compatibility
        rating_map = {
            'ATTRACTIVE for income investors': 'Excellent',
            'GOOD for balanced portfolios': 'Good',
            'ACCEPTABLE': 'Fair',
            'Evaluate for growth potential instead': 'Fair'
        }
        
        return {
            'dividend_yield': round(dividend_yield, 4),
            'yield_percentage': round(yield_percentage, 2),
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation,
            'rating': rating_map.get(recommendation, 'Fair')
        }
    
    def comprehensive_analysis(self, stock_data):
        """
        Perform comprehensive fundamental analysis on a stock.
        
        Args:
            stock_data: Dictionary containing:
                - price: Current price
                - eps: Earnings per share
                - book_value_per_share: Book value per share
                - net_income: Annual net income
                - shareholders_equity: Shareholders' equity
                - total_debt: Total debt
                - current_assets: Current assets
                - current_liabilities: Current liabilities
                - previous_eps: Previous year EPS (optional)
                - annual_dividend: Annual dividend per share (optional)
        
        Returns:
            dict: Complete fundamental analysis with overall score
        """
        results = {}
        
        # Calculate P/E ratio
        if 'price' in stock_data and 'eps' in stock_data:
            results['pe_ratio'] = self.calculate_pe_ratio(
                stock_data['price'], stock_data['eps']
            )
        
        # Calculate P/B ratio
        if 'price' in stock_data and 'book_value_per_share' in stock_data:
            results['pb_ratio'] = self.calculate_pb_ratio(
                stock_data['price'], stock_data['book_value_per_share']
            )
        
        # Calculate ROE
        if 'net_income' in stock_data and 'shareholders_equity' in stock_data:
            results['roe'] = self.calculate_roe(
                stock_data['net_income'], stock_data['shareholders_equity']
            )
        
        # Calculate D/E ratio
        if 'total_debt' in stock_data and 'shareholders_equity' in stock_data:
            results['debt_to_equity'] = self.calculate_debt_to_equity(
                stock_data['total_debt'], stock_data['shareholders_equity']
            )
        
        # Calculate Current Ratio
        if 'current_assets' in stock_data and 'current_liabilities' in stock_data:
            results['current_ratio'] = self.calculate_current_ratio(
                stock_data['current_assets'], stock_data['current_liabilities']
            )
        
        # Calculate Earnings Growth
        if 'eps' in stock_data and 'previous_eps' in stock_data:
            results['earnings_growth'] = self.calculate_earnings_growth(
                stock_data['eps'], stock_data['previous_eps']
            )
        
        # Calculate Dividend Yield
        if 'price' in stock_data and 'annual_dividend' in stock_data:
            results['dividend_yield'] = self.calculate_dividend_yield(
                stock_data['annual_dividend'], stock_data['price']
            )
        
        # Calculate overall fundamental score (weighted average)
        scores = []
        for metric_name, metric_data in results.items():
            if isinstance(metric_data, dict) and 'score' in metric_data:
                scores.append(metric_data['score'])
        
        if scores:
            overall_score = sum(scores) / len(scores)
        else:
            overall_score = 0
        
        # Overall recommendation based on score
        if overall_score >= 85:
            overall_recommendation = 'STRONG BUY - Excellent fundamentals'
        elif overall_score >= 75:
            overall_recommendation = 'BUY - Strong fundamentals'
        elif overall_score >= 60:
            overall_recommendation = 'HOLD - Acceptable fundamentals'
        elif overall_score >= 45:
            overall_recommendation = 'HOLD/SELL - Weak fundamentals'
        else:
            overall_recommendation = 'SELL - Poor fundamentals'
        
        return {
            'metrics': results,
            'overall_score': round(overall_score, 2),
            'overall_recommendation': overall_recommendation,
            'metrics_analyzed': len(results)
        }
