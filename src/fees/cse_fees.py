"""
CSE (Colombo Stock Exchange) Fee Calculator Module.

This module calculates all trading fees and taxes applicable to CSE trades,
including broker commission, SEC fee, exchange fee, CDS fee, STL tax, and
capital gains tax.
"""

from src.utils.helpers import load_config, validate_positive_number


class CSEFeeCalculator:
    """Calculate CSE trading fees and taxes."""
    
    def __init__(self, custom_config=None):
        """
        Initialize fee calculator with configuration.
        
        Args:
            custom_config: Optional dictionary to override default config
        """
        self.config = custom_config if custom_config else load_config()
    
    def _get_fee_rates(self, transaction_value):
        """
        Get the appropriate fee rates based on transaction value.
        
        Args:
            transaction_value: Total transaction value
        
        Returns:
            dict: Fee rates for the transaction tier
        """
        if transaction_value <= self.config['cse_fees']['tier_1']['max_value']:
            # Tier 1: Up to Rs. 100Mn
            tier = self.config['cse_fees']['tier_1']
        else:
            # Tier 2: Over Rs. 100Mn
            tier = self.config['cse_fees']['tier_2']
        
        return {
            'broker_commission': tier['broker_commission'],
            'sec_fee': tier['sec_fee'],
            'cse_fee': tier['cse_fee'],
            'cds_fee': tier['cds_fee'],
            'stl_tax': tier['stl_tax']
        }
    
    def calculate_buy_fees(self, transaction_value, quantity=1):
        """
        Calculate total fees when buying shares.
        
        Args:
            transaction_value: Total value of shares purchased (price * quantity)
            quantity: Number of shares (default: 1)
        
        Returns:
            dict: Breakdown of all buy-side fees
        """
        validate_positive_number(transaction_value, "Transaction value")
        
        # Get appropriate fee rates for this transaction value
        rates = self._get_fee_rates(transaction_value)
        
        # Calculate each fee component
        broker_commission = transaction_value * rates['broker_commission']
        broker_commission = max(broker_commission, self.config['cse_fees']['minimum_commission'])
        
        sec_fee = transaction_value * rates['sec_fee']
        cse_fee = transaction_value * rates['cse_fee']
        cds_fee = transaction_value * rates['cds_fee']
        
        total_fees = broker_commission + sec_fee + cse_fee + cds_fee
        total_cost = transaction_value + total_fees
        
        return {
            'transaction_value': transaction_value,
            'broker_commission': broker_commission,
            'sec_fee': sec_fee,
            'cse_fee': cse_fee,
            'cds_fee': cds_fee,
            'total_fees': total_fees,
            'total_cost': total_cost,
            'effective_rate': total_fees / transaction_value if transaction_value > 0 else 0,
            'tier': 'Tier 1 (≤ Rs. 100Mn)' if transaction_value <= self.config['cse_fees']['tier_1']['max_value'] else 'Tier 2 (> Rs. 100Mn)'
        }
    
    def calculate_sell_fees(self, transaction_value, quantity=1):
        """
        Calculate total fees when selling shares (includes STL tax).
        
        Args:
            transaction_value: Total value of shares sold (price * quantity)
            quantity: Number of shares (default: 1)
        
        Returns:
            dict: Breakdown of all sell-side fees
        """
        validate_positive_number(transaction_value, "Transaction value")
        
        # Get appropriate fee rates for this transaction value
        rates = self._get_fee_rates(transaction_value)
        
        # Calculate each fee component
        broker_commission = transaction_value * rates['broker_commission']
        broker_commission = max(broker_commission, self.config['cse_fees']['minimum_commission'])
        
        sec_fee = transaction_value * rates['sec_fee']
        cse_fee = transaction_value * rates['cse_fee']
        cds_fee = transaction_value * rates['cds_fee']
        stl_tax = transaction_value * rates['stl_tax']  # Only on sell
        
        total_fees = broker_commission + sec_fee + cse_fee + cds_fee + stl_tax
        net_proceeds = transaction_value - total_fees
        
        return {
            'transaction_value': transaction_value,
            'broker_commission': broker_commission,
            'sec_fee': sec_fee,
            'cse_fee': cse_fee,
            'cds_fee': cds_fee,
            'stl_tax': stl_tax,
            'total_fees': total_fees,
            'net_proceeds': net_proceeds,
            'effective_rate': total_fees / transaction_value if transaction_value > 0 else 0,
            'tier': 'Tier 1 (≤ Rs. 100Mn)' if transaction_value <= self.config['cse_fees']['tier_1']['max_value'] else 'Tier 2 (> Rs. 100Mn)'
        }
    
    def calculate_capital_gains_tax(self, capital_gain):
        """
        Calculate capital gains tax on profit.
        
        Args:
            capital_gain: Profit from the trade (can be negative for loss)
        
        Returns:
            dict: Capital gains tax details
        """
        if capital_gain <= 0:
            return {
                'capital_gain': capital_gain,
                'tax_rate': 0,
                'tax_amount': 0,
                'net_profit_after_tax': capital_gain
            }
        
        tax_amount = capital_gain * self.config['taxes']['capital_gains_tax']
        net_profit = capital_gain - tax_amount
        
        return {
            'capital_gain': capital_gain,
            'tax_rate': self.config['taxes']['capital_gains_tax'],
            'tax_amount': tax_amount,
            'net_profit_after_tax': net_profit
        }
    
    def calculate_round_trip_cost(self, buy_price, sell_price, quantity):
        """
        Calculate total cost for a complete buy-sell transaction.
        
        Args:
            buy_price: Price per share when buying
            sell_price: Price per share when selling
            quantity: Number of shares
        
        Returns:
            dict: Complete breakdown of round-trip transaction
        """
        validate_positive_number(buy_price, "Buy price")
        validate_positive_number(sell_price, "Sell price")
        validate_positive_number(quantity, "Quantity")
        
        # Calculate buy side
        buy_value = buy_price * quantity
        buy_fees_detail = self.calculate_buy_fees(buy_value, quantity)
        
        # Calculate sell side
        sell_value = sell_price * quantity
        sell_fees_detail = self.calculate_sell_fees(sell_value, quantity)
        
        # Calculate profit/loss before tax
        gross_profit = sell_fees_detail['net_proceeds'] - buy_fees_detail['total_cost']
        
        # Calculate capital gains tax
        tax_detail = self.calculate_capital_gains_tax(gross_profit)
        
        # Total fees
        total_fees = buy_fees_detail['total_fees'] + sell_fees_detail['total_fees']
        
        return {
            'buy_price': buy_price,
            'sell_price': sell_price,
            'quantity': quantity,
            'buy_value': buy_value,
            'buy_fees': buy_fees_detail,
            'sell_value': sell_value,
            'sell_fees': sell_fees_detail,
            'total_fees': total_fees,
            'gross_profit': gross_profit,
            'capital_gains_tax': tax_detail,
            'net_profit': tax_detail['net_profit_after_tax'],
            'total_cost_percentage': (total_fees / buy_value * 100) if buy_value > 0 else 0
        }
    
    def get_fee_summary(self):
        """
        Get a summary of current fee structure.
        
        Returns:
            dict: All fee rates and minimums
        """
        tier1 = self.config['cse_fees']['tier_1']
        tier2 = self.config['cse_fees']['tier_2']
        
        return {
            'tier_1_max': f"LKR {tier1['max_value']:,.0f}",
            'tier_1_brokerage': f"{tier1['broker_commission'] * 100}%",
            'tier_1_cse': f"{tier1['cse_fee'] * 100}%",
            'tier_1_cds': f"{tier1['cds_fee'] * 100}%",
            'tier_1_sec': f"{tier1['sec_fee'] * 100}%",
            'tier_1_stl': f"{tier1['stl_tax'] * 100}% (sell only)",
            'tier_1_total': f"{(tier1['broker_commission'] + tier1['cse_fee'] + tier1['cds_fee'] + tier1['sec_fee']) * 100}%",
            
            'tier_2_min': f"LKR {tier2['min_value']:,.0f}+",
            'tier_2_brokerage': f"{tier2['broker_commission'] * 100}%",
            'tier_2_cse': f"{tier2['cse_fee'] * 100}%",
            'tier_2_cds': f"{tier2['cds_fee'] * 100}%",
            'tier_2_sec': f"{tier2['sec_fee'] * 100}%",
            'tier_2_stl': f"{tier2['stl_tax'] * 100}% (sell only)",
            'tier_2_total': f"{(tier2['broker_commission'] + tier2['cse_fee'] + tier2['cds_fee'] + tier2['sec_fee']) * 100}%",
            
            'capital_gains_tax': f"{self.config['taxes']['capital_gains_tax'] * 100}%",
            'minimum_commission': f"LKR {self.config['cse_fees']['minimum_commission']}"
        }


def calculate_buy_fees(buy_price, quantity, custom_config=None):
    """
    Convenience function to calculate buy fees.
    
    Args:
        buy_price: Price per share
        quantity: Number of shares
        custom_config: Optional custom configuration
    
    Returns:
        dict: Buy fees breakdown
    """
    calculator = CSEFeeCalculator(custom_config)
    transaction_value = buy_price * quantity
    return calculator.calculate_buy_fees(transaction_value, quantity)


def calculate_sell_fees(sell_price, quantity, custom_config=None):
    """
    Convenience function to calculate sell fees.
    
    Args:
        sell_price: Price per share
        quantity: Number of shares
        custom_config: Optional custom configuration
    
    Returns:
        dict: Sell fees breakdown
    """
    calculator = CSEFeeCalculator(custom_config)
    transaction_value = sell_price * quantity
    return calculator.calculate_sell_fees(transaction_value, quantity)
