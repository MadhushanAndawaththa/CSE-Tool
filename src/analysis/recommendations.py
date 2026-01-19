"""
Stock Recommendation Engine.

This module combines fundamental analysis, technical analysis, and risk assessment
to generate comprehensive buy/sell/hold recommendations with scoring and rationale.
"""

from src.calculations.fundamental import FundamentalAnalyzer
from src.calculations.technical import TechnicalAnalyzer
from src.calculations.breakeven import BreakEvenCalculator
from src.utils.helpers import load_config


class RecommendationEngine:
    """Generate stock recommendations based on comprehensive analysis."""
    
    def __init__(self, custom_config=None):
        """
        Initialize recommendation engine.
        
        Args:
            custom_config: Optional dictionary to override default config
        """
        self.config = custom_config if custom_config else load_config()
        self.fundamental_analyzer = FundamentalAnalyzer(custom_config)
        self.technical_analyzer = TechnicalAnalyzer(custom_config)
        self.breakeven_calculator = BreakEvenCalculator(custom_config)
        
        # Get weights from config
        self.weights = self.config['thresholds']['weights']
    
    def calculate_risk_score(self, stock_data):
        """
        Calculate risk score based on various risk factors.
        
        Args:
            stock_data: Dictionary containing risk-related data:
                - debt_to_equity_ratio: Debt to equity ratio
                - current_ratio: Current ratio
                - beta: Stock beta (volatility vs market) - optional
                - market_cap: Market capitalization - optional
        
        Returns:
            dict: Risk assessment with score
        """
        risk_factors = []
        risk_details = []
        
        # Debt-to-equity risk (lower is better)
        if 'debt_to_equity_ratio' in stock_data:
            de_ratio = stock_data['debt_to_equity_ratio']
            if de_ratio <= 0.5:
                de_score = 90
                risk_details.append('Low leverage (excellent)')
            elif de_ratio <= 1.0:
                de_score = 75
                risk_details.append('Moderate leverage (good)')
            elif de_ratio <= 1.5:
                de_score = 55
                risk_details.append('Elevated leverage (caution)')
            elif de_ratio <= 2.0:
                de_score = 35
                risk_details.append('High leverage (risky)')
            else:
                de_score = 15
                risk_details.append('Very high leverage (high risk)')
            risk_factors.append(de_score)
        
        # Liquidity risk (higher current ratio is better)
        if 'current_ratio' in stock_data:
            cr = stock_data['current_ratio']
            if cr >= 2.0:
                cr_score = 90
                risk_details.append('Strong liquidity')
            elif cr >= 1.5:
                cr_score = 75
                risk_details.append('Adequate liquidity')
            elif cr >= 1.0:
                cr_score = 50
                risk_details.append('Marginal liquidity')
            else:
                cr_score = 25
                risk_details.append('Liquidity concerns')
            risk_factors.append(cr_score)
        
        # Beta risk (if available)
        if 'beta' in stock_data:
            beta = stock_data['beta']
            if beta <= 0.8:
                beta_score = 85
                risk_details.append('Low volatility')
            elif beta <= 1.2:
                beta_score = 70
                risk_details.append('Average volatility')
            elif beta <= 1.5:
                beta_score = 50
                risk_details.append('Above average volatility')
            else:
                beta_score = 30
                risk_details.append('High volatility')
            risk_factors.append(beta_score)
        
        # Market cap risk (larger = generally less risky)
        if 'market_cap' in stock_data:
            market_cap = stock_data['market_cap']
            if market_cap >= 10_000_000_000:  # 10B+ LKR
                mc_score = 85
                risk_details.append('Large cap (stable)')
            elif market_cap >= 1_000_000_000:  # 1B+ LKR
                mc_score = 70
                risk_details.append('Mid cap (moderate risk)')
            else:
                mc_score = 50
                risk_details.append('Small cap (higher risk)')
            risk_factors.append(mc_score)
        
        # Calculate overall risk score
        if risk_factors:
            risk_score = sum(risk_factors) / len(risk_factors)
        else:
            risk_score = 50  # Neutral if no data
            risk_details.append('Insufficient data for risk assessment')
        
        # Risk level interpretation
        if risk_score >= 75:
            risk_level = 'LOW RISK'
            risk_interpretation = 'Conservative investment with low risk profile'
        elif risk_score >= 60:
            risk_level = 'MODERATE RISK'
            risk_interpretation = 'Balanced risk-reward profile'
        elif risk_score >= 45:
            risk_level = 'ELEVATED RISK'
            risk_interpretation = 'Higher risk factors present'
        else:
            risk_level = 'HIGH RISK'
            risk_interpretation = 'Significant risk factors - suitable for aggressive investors only'
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'risk_interpretation': risk_interpretation,
            'risk_factors': risk_details,
            'factors_analyzed': len(risk_factors)
        }
    
    def generate_recommendation(self, stock_data, prices=None, volumes=None):
        """
        Generate comprehensive stock recommendation.
        
        Args:
            stock_data: Dictionary containing fundamental data:
                Required for fundamental:
                - price, eps, book_value_per_share, net_income, shareholders_equity,
                  total_debt, current_assets, current_liabilities
                Optional:
                - previous_eps, annual_dividend, beta, market_cap
                - ticker (stock symbol)
                - company_name
            prices: List of historical prices for technical analysis
            volumes: List of trading volumes (optional)
        
        Returns:
            dict: Complete recommendation with scores and rationale
        """
        recommendation = {
            'stock_info': {},
            'fundamental_analysis': None,
            'technical_analysis': None,
            'risk_assessment': None,
            'overall_score': 0,
            'recommendation': 'N/A',
            'confidence': 'N/A',
            'key_strengths': [],
            'key_concerns': [],
            'action_items': []
        }
        
        # Store stock info
        if 'ticker' in stock_data:
            recommendation['stock_info']['ticker'] = stock_data['ticker']
        if 'company_name' in stock_data:
            recommendation['stock_info']['company_name'] = stock_data['company_name']
        if 'price' in stock_data:
            recommendation['stock_info']['current_price'] = stock_data['price']
        
        # Perform fundamental analysis
        fundamental_result = self.fundamental_analyzer.comprehensive_analysis(stock_data)
        recommendation['fundamental_analysis'] = fundamental_result
        fundamental_score = fundamental_result['overall_score']
        
        # Perform technical analysis (if price data provided)
        if prices and len(prices) > 0:
            technical_result = self.technical_analyzer.comprehensive_analysis(prices, volumes)
            recommendation['technical_analysis'] = technical_result
            technical_score = technical_result['overall_score']
        else:
            technical_score = 50  # Neutral if no technical data
            recommendation['technical_analysis'] = {
                'overall_score': 50,
                'overall_signal': 'NEUTRAL',
                'overall_recommendation': 'No price history provided'
            }
        
        # Perform risk assessment
        risk_result = self.calculate_risk_score(stock_data)
        recommendation['risk_assessment'] = risk_result
        risk_score = risk_result['risk_score']
        
        # Calculate weighted overall score
        overall_score = (
            fundamental_score * self.weights['fundamental'] +
            technical_score * self.weights['technical'] +
            risk_score * self.weights['risk']
        )
        recommendation['overall_score'] = round(overall_score, 2)
        
        # Generate overall recommendation
        if overall_score >= 80:
            recommendation['recommendation'] = 'STRONG BUY'
            recommendation['confidence'] = 'HIGH'
            recommendation['action_items'].append('Consider establishing or adding to position')
        elif overall_score >= 70:
            recommendation['recommendation'] = 'BUY'
            recommendation['confidence'] = 'MODERATE-HIGH'
            recommendation['action_items'].append('Good opportunity to buy')
        elif overall_score >= 55:
            recommendation['recommendation'] = 'HOLD'
            recommendation['confidence'] = 'MODERATE'
            recommendation['action_items'].append('Maintain current position if owned')
            recommendation['action_items'].append('Wait for better entry point if not owned')
        elif overall_score >= 40:
            recommendation['recommendation'] = 'SELL'
            recommendation['confidence'] = 'MODERATE-HIGH'
            recommendation['action_items'].append('Consider reducing position')
        else:
            recommendation['recommendation'] = 'STRONG SELL'
            recommendation['confidence'] = 'HIGH'
            recommendation['action_items'].append('Exit position or avoid purchasing')
        
        # Identify key strengths
        if fundamental_score >= 75:
            recommendation['key_strengths'].append('Strong fundamental metrics')
        if technical_score >= 70:
            recommendation['key_strengths'].append('Positive technical indicators')
        if risk_score >= 70:
            recommendation['key_strengths'].append('Low risk profile')
        
        # Add specific strengths from fundamental analysis
        if fundamental_result.get('metrics'):
            for metric_name, metric_data in fundamental_result['metrics'].items():
                if isinstance(metric_data, dict) and metric_data.get('score', 0) >= 80:
                    recommendation['key_strengths'].append(
                        f"{metric_name.upper()}: {metric_data.get('interpretation', 'Good')}"
                    )
        
        # Identify key concerns
        if fundamental_score < 50:
            recommendation['key_concerns'].append('Weak fundamental metrics')
        if technical_score < 45:
            recommendation['key_concerns'].append('Negative technical signals')
        if risk_score < 50:
            recommendation['key_concerns'].append('Elevated risk factors')
        
        # Add specific concerns from fundamental analysis
        if fundamental_result.get('metrics'):
            for metric_name, metric_data in fundamental_result['metrics'].items():
                if isinstance(metric_data, dict) and metric_data.get('score', 100) <= 40:
                    recommendation['key_concerns'].append(
                        f"{metric_name.upper()}: {metric_data.get('interpretation', 'Concerning')}"
                    )
        
        # Add risk-specific concerns
        if risk_result.get('risk_factors'):
            for factor in risk_result['risk_factors']:
                if 'high' in factor.lower() or 'concern' in factor.lower():
                    recommendation['key_concerns'].append(factor)
        
        # Limit to top 5 strengths and concerns for readability
        recommendation['key_strengths'] = recommendation['key_strengths'][:5]
        recommendation['key_concerns'] = recommendation['key_concerns'][:5]
        
        return recommendation
    
    def compare_to_breakeven(self, stock_data, buy_price, quantity):
        """
        Compare current price to break-even and provide recommendation.
        
        Args:
            stock_data: Stock data dictionary
            buy_price: Original purchase price
            quantity: Number of shares owned
        
        Returns:
            dict: Comparison and recommendation
        """
        current_price = stock_data.get('price')
        if not current_price:
            return {
                'error': 'Current price not provided'
            }
        
        # Calculate break-even
        breakeven_result = self.breakeven_calculator.calculate_breakeven_price(
            buy_price, quantity, include_tax=True
        )
        
        breakeven_price = breakeven_result['breakeven_price']
        
        # Calculate current profit/loss
        profit_result = self.breakeven_calculator.calculate_profit_at_price(
            buy_price, current_price, quantity, include_tax=True
        )
        
        # Determine recommendation based on position
        if current_price >= breakeven_price:
            position_status = 'PROFITABLE'
            if profit_result['profit_percentage'] >= 20:
                position_recommendation = 'Consider taking profits - strong gains achieved'
            elif profit_result['profit_percentage'] >= 10:
                position_recommendation = 'Moderate profits - hold for further gains or take profits'
            else:
                position_recommendation = 'Slightly above break-even - hold for better returns'
        else:
            position_status = 'LOSS'
            loss_percentage = abs(profit_result['profit_percentage'])
            if loss_percentage >= 20:
                position_recommendation = 'Significant loss - evaluate if fundamentals support recovery'
            elif loss_percentage >= 10:
                position_recommendation = 'Moderate loss - hold if fundamentals are strong'
            else:
                position_recommendation = 'Small loss - near break-even, consider holding'
        
        return {
            'buy_price': buy_price,
            'current_price': current_price,
            'breakeven_price': breakeven_price,
            'quantity': quantity,
            'position_status': position_status,
            'current_profit_loss': profit_result['net_profit'],
            'profit_percentage': profit_result['profit_percentage'],
            'price_to_breakeven': current_price - breakeven_price,
            'position_recommendation': position_recommendation,
            'breakeven_details': breakeven_result,
            'profit_details': profit_result
        }
    
    def calculate_entry_price(self, stock_data, target_profit_percentage=15):
        """
        Calculate ideal entry price for a target profit.
        
        Args:
            stock_data: Stock data dictionary with 'price' (current price)
            target_profit_percentage: Desired profit percentage
        
        Returns:
            dict: Entry price recommendation
        """
        current_price = stock_data.get('price')
        if not current_price:
            return {'error': 'Current price not provided'}
        
        # Perform analysis to get recommendation
        recommendation = self.generate_recommendation(stock_data)
        
        # Calculate ideal entry price based on recommendation
        if recommendation['overall_score'] >= 70:
            # Good buy - current price is acceptable
            max_entry_price = current_price * 1.05  # Up to 5% above current
            ideal_entry = current_price
            entry_recommendation = 'Strong fundamentals - current price is good entry point'
        elif recommendation['overall_score'] >= 55:
            # Hold - wait for better price
            max_entry_price = current_price * 0.95  # 5% below current
            ideal_entry = current_price * 0.97  # 3% below
            entry_recommendation = 'Wait for 3-5% pullback for better entry'
        else:
            # Weak - need significant discount
            max_entry_price = current_price * 0.90  # 10% below current
            ideal_entry = current_price * 0.85  # 15% below
            entry_recommendation = 'Weak fundamentals - only buy at significant discount (10-15% lower)'
        
        return {
            'current_price': current_price,
            'ideal_entry_price': round(ideal_entry, 2),
            'max_entry_price': round(max_entry_price, 2),
            'target_profit_percentage': target_profit_percentage,
            'entry_recommendation': entry_recommendation,
            'overall_score': recommendation['overall_score'],
            'overall_recommendation': recommendation['recommendation']
        }
