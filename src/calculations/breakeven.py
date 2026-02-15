"""
Break-Even Price Calculator for CSE Stocks.

This module calculates the minimum selling price needed to break even
after accounting for all CSE trading fees and taxes.
"""

from src.fees.cse_fees import CSEFeeCalculator
from src.utils.helpers import validate_positive_number
from typing import Any, Dict, Optional

# Constants for iterative calculations
MAX_ITERATIONS = 20  # Maximum iterations for break-even convergence
CONVERGENCE_TOLERANCE = 0.01  # Tolerance for profit calculation (LKR)


class BreakEvenCalculator:
    """Calculate break-even price for stock positions."""
    
    def __init__(self, custom_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize break-even calculator.
        
        Args:
            custom_config: Optional dictionary to override default config
        """
        self.fee_calculator = CSEFeeCalculator(custom_config)
        self.config = self.fee_calculator.config
    
    def calculate_breakeven_price(self, buy_price: float, quantity: float, include_tax: bool = True) -> Dict[str, Any]:
        """
        Calculate the minimum selling price to break even.
        
        The break-even price accounts for:
        - All buying fees (commission, SEC fee, exchange fee, CDS fee)
        - All selling fees (commission, SEC fee, exchange fee, CDS fee, STL tax)
        - Capital gains tax (if include_tax=True)
        
        Args:
            buy_price: Original purchase price per share
            quantity: Number of shares purchased
            include_tax: Whether to include capital gains tax in calculation
        
        Returns:
            dict: Break-even analysis with detailed calculations
        """
        validate_positive_number(buy_price, "Buy price")
        validate_positive_number(quantity, "Quantity")
        
        # Calculate total cost of buying
        buy_value = buy_price * quantity
        buy_fees = self.fee_calculator.calculate_buy_fees(buy_value, quantity)
        total_investment = buy_fees['total_cost']
        
        # To break even, we need: net_proceeds_from_sale >= total_investment
        # If including tax: net_proceeds_after_tax >= total_investment
        
        # Get fee rates for selling (use buy_value as reference for tier determination)
        rates = self.fee_calculator._get_fee_rates(buy_value)
        
        # Selling fee rate (excluding STL which is already in the rate)
        sell_fee_rate = (
            rates['broker_commission'] +
            rates['sec_fee'] +
            rates['cse_fee'] +
            rates['cds_fee'] +
            rates['stl_tax']
        )
        
        # Validate that fee rate is not 100% or higher (would make break-even impossible)
        if sell_fee_rate >= 1.0:
            raise ValueError(f"Total selling fee rate ({sell_fee_rate * 100:.2f}%) is too high. Break-even calculation impossible.")
        
        if not include_tax:
            # Break-even without considering capital gains tax
            # sell_price * quantity * (1 - sell_fee_rate) = total_investment
            # sell_price = total_investment / (quantity * (1 - sell_fee_rate))
            
            breakeven_price = total_investment / (quantity * (1 - sell_fee_rate))
            
            # Verify calculation
            sell_fees = self.fee_calculator.calculate_sell_fees(
                breakeven_price * quantity, quantity
            )
            net_proceeds = sell_fees['net_proceeds']
            profit = net_proceeds - total_investment
            
            return {
                'buy_price': buy_price,
                'quantity': quantity,
                'total_investment': total_investment,
                'buy_fees_paid': buy_fees['total_fees'],
                'breakeven_price': breakeven_price,
                'sell_value_at_breakeven': breakeven_price * quantity,
                'sell_fees_at_breakeven': sell_fees['total_fees'],
                'net_proceeds': net_proceeds,
                'profit_at_breakeven': profit,
                'price_increase_required': breakeven_price - buy_price,
                'price_increase_percentage': (breakeven_price - buy_price) / buy_price,
                'includes_capital_gains_tax': False
            }
        
        else:
            # Break-even including capital gains tax (more complex)
            # We need to solve iteratively because tax is on profit
            
            # Start with estimate without tax
            estimate = total_investment / (quantity * (1 - sell_fee_rate))
            
            # Iteratively refine to include tax on the profit
            for iteration in range(MAX_ITERATIONS):  # Usually converges in 2-3 iterations
                sell_value = estimate * quantity
                sell_fees_detail = self.fee_calculator.calculate_sell_fees(sell_value, quantity)
                gross_profit = sell_fees_detail['net_proceeds'] - total_investment
                
                if gross_profit > 0:
                    tax = gross_profit * self.fee_calculator.config['taxes']['capital_gains_tax']
                    net_profit = gross_profit - tax
                    
                    # Adjust estimate to make net_profit = 0
                    if abs(net_profit) < CONVERGENCE_TOLERANCE:  # Close enough
                        break
                    
                    # Need to increase sell price to cover the tax
                    adjustment = tax / quantity
                    estimate += adjustment / (1 - sell_fee_rate)
                else:
                    # No profit, no tax
                    break
            
            breakeven_price = estimate
            
            # Final verification
            sell_value = breakeven_price * quantity
            sell_fees = self.fee_calculator.calculate_sell_fees(sell_value, quantity)
            gross_profit = sell_fees['net_proceeds'] - total_investment
            tax_detail = self.fee_calculator.calculate_capital_gains_tax(gross_profit)
            net_profit = tax_detail['net_profit_after_tax']
            
            return {
                'buy_price': buy_price,
                'quantity': quantity,
                'total_investment': total_investment,
                'buy_fees_paid': buy_fees['total_fees'],
                'breakeven_price': breakeven_price,
                'sell_value_at_breakeven': sell_value,
                'sell_fees_at_breakeven': sell_fees['total_fees'],
                'net_proceeds': sell_fees['net_proceeds'],
                'gross_profit': gross_profit,
                'capital_gains_tax': tax_detail['tax_amount'],
                'net_profit_after_tax': net_profit,
                'price_increase_required': breakeven_price - buy_price,
                'price_increase_percentage': (breakeven_price - buy_price) / buy_price,
                'includes_capital_gains_tax': True
            }
    
    def calculate_target_price(self, buy_price, quantity, target_profit_percentage,
                               include_tax=True):
        """
        Calculate the selling price needed to achieve a target profit percentage.
        
        Args:
            buy_price: Original purchase price per share
            quantity: Number of shares
            target_profit_percentage: Desired profit as percentage of investment (e.g., 20 for 20%)
            include_tax: Whether to include capital gains tax
        
        Returns:
            dict: Target price analysis
        """
        validate_positive_number(buy_price, "Buy price")
        validate_positive_number(quantity, "Quantity")
        validate_positive_number(target_profit_percentage, "Target profit percentage")
        
        # Get break-even details
        breakeven = self.calculate_breakeven_price(buy_price, quantity, include_tax)
        
        # Calculate required net profit
        total_investment = breakeven['total_investment']
        required_net_profit = total_investment * (target_profit_percentage / 100)
        
        # If including tax, we need gross profit such that:
        # gross_profit * (1 - tax_rate) = required_net_profit
        if include_tax and required_net_profit > 0:
            tax_rate = self.fee_calculator.config['taxes']['capital_gains_tax']
            required_gross_profit = required_net_profit / (1 - tax_rate)
        else:
            required_gross_profit = required_net_profit
        
        # Required net proceeds from sale
        required_net_proceeds = total_investment + required_gross_profit
        
        # Calculate sell price needed to get this net proceeds
        # Working backwards from net_proceeds
        rates = self.fee_calculator._get_fee_rates(required_net_proceeds)
        sell_fee_rate = (
            rates['broker_commission'] +
            rates['sec_fee'] +
            rates['cse_fee'] +
            rates['cds_fee'] +
            rates['stl_tax']
        )
        
        target_sell_price = required_net_proceeds / (quantity * (1 - sell_fee_rate))
        
        # Verify
        sell_fees = self.fee_calculator.calculate_sell_fees(
            target_sell_price * quantity, quantity
        )
        actual_gross_profit = sell_fees['net_proceeds'] - total_investment
        
        if include_tax:
            tax_detail = self.fee_calculator.calculate_capital_gains_tax(actual_gross_profit)
            actual_net_profit = tax_detail['net_profit_after_tax']
            actual_tax = tax_detail['tax_amount']
        else:
            actual_net_profit = actual_gross_profit
            actual_tax = 0
        
        actual_profit_percentage = (actual_net_profit / total_investment) * 100
        
        return {
            'buy_price': buy_price,
            'quantity': quantity,
            'total_investment': total_investment,
            'target_profit_percentage': target_profit_percentage,
            'target_profit_amount': required_net_profit,
            'target_sell_price': target_sell_price,
            'breakeven_price': breakeven['breakeven_price'],
            'price_increase_from_buy': target_sell_price - buy_price,
            'price_increase_percentage': (target_sell_price - buy_price) / buy_price,
            'price_above_breakeven': target_sell_price - breakeven['breakeven_price'],
            'sell_fees': sell_fees['total_fees'],
            'gross_profit': actual_gross_profit,
            'capital_gains_tax': actual_tax,
            'net_profit': actual_net_profit,
            'actual_profit_percentage': actual_profit_percentage,
            'includes_capital_gains_tax': include_tax
        }
    
    def calculate_profit_at_price(self, buy_price, sell_price, quantity, include_tax=True):
        """
        Calculate profit/loss if selling at a specific price.
        
        Args:
            buy_price: Original purchase price per share
            sell_price: Proposed selling price per share
            quantity: Number of shares
            include_tax: Whether to include capital gains tax
        
        Returns:
            dict: Profit/loss analysis
        """
        validate_positive_number(buy_price, "Buy price")
        validate_positive_number(sell_price, "Sell price")
        validate_positive_number(quantity, "Quantity")
        
        # Calculate complete round trip
        round_trip = self.fee_calculator.calculate_round_trip_cost(
            buy_price, sell_price, quantity
        )
        
        breakeven = self.calculate_breakeven_price(buy_price, quantity, include_tax)
        
        if include_tax:
            net_profit = round_trip['net_profit']
        else:
            net_profit = round_trip['gross_profit']
        
        profit_percentage = (net_profit / round_trip['buy_fees']['total_cost'])
        
        return {
            'buy_price': buy_price,
            'sell_price': sell_price,
            'quantity': quantity,
            'total_investment': round_trip['buy_fees']['total_cost'],
            'total_fees': round_trip['total_fees'],
            'gross_profit': round_trip['gross_profit'],
            'capital_gains_tax': round_trip['capital_gains_tax']['tax_amount'],
            'net_profit': net_profit,
            'profit_percentage': profit_percentage,
            'breakeven_price': breakeven['breakeven_price'],
            'above_breakeven': sell_price >= breakeven['breakeven_price'],
            'price_vs_breakeven': sell_price - breakeven['breakeven_price'],
            'includes_capital_gains_tax': include_tax
        }


def calculate_breakeven(buy_price, quantity, include_tax=True, custom_config=None):
    """
    Convenience function to calculate break-even price.
    
    Args:
        buy_price: Purchase price per share
        quantity: Number of shares
        include_tax: Include capital gains tax in calculation
        custom_config: Optional custom configuration
    
    Returns:
        dict: Break-even analysis
    """
    calculator = BreakEvenCalculator(custom_config)
    return calculator.calculate_breakeven_price(buy_price, quantity, include_tax)
