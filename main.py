"""
Main CLI Application for CSE Stock Analyzer.

This is the main entry point for the command-line interface.
"""

import sys
from tabulate import tabulate
from colorama import init, Fore, Style

from src.calculations.breakeven import BreakEvenCalculator
from src.calculations.fundamental import FundamentalAnalyzer
from src.calculations.technical import TechnicalAnalyzer
from src.analysis.recommendations import RecommendationEngine
from src.fees.cse_fees import CSEFeeCalculator
from src.utils.helpers import format_currency, format_percentage, color_text
from src.utils.logger import setup_logging, get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize colorama for Windows support
init(autoreset=True)


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(color_text(f"  {text}", 'cyan'))
    print("=" * 70 + "\n")


def print_section(text):
    """Print a formatted section header."""
    print("\n" + color_text(f">>> {text}", 'yellow'))
    print("-" * 70)


def get_float_input(prompt, default=None, allow_zero=False):
    """Get float input from user with validation."""
    while True:
        user_input = input(prompt)
        if not user_input and default is not None:
            return default
        try:
            value = float(user_input)
            if not allow_zero and value <= 0:
                print(color_text("Please enter a positive number.", 'red'))
                continue
            if allow_zero and value < 0:
                print(color_text("Please enter a non-negative number.", 'red'))
                continue
            return value
        except ValueError:
            print(color_text("Invalid input. Please enter a number.", 'red'))


def get_int_input(prompt, default=None):
    """Get integer input from user with validation."""
    while True:
        user_input = input(prompt)
        if not user_input and default is not None:
            return default
        try:
            value = int(user_input)
            if value <= 0:
                print(color_text("Please enter a positive integer.", 'red'))
                continue
            return value
        except ValueError:
            print(color_text("Invalid input. Please enter an integer.", 'red'))


def get_price_list():
    """Get list of historical prices from user."""
    print("\nEnter historical prices (most recent last).")
    print("Enter prices one per line. Type 'done' when finished.")
    prices = []
    while True:
        user_input = input(f"Price {len(prices) + 1} (or 'done'): ")
        if user_input.lower() == 'done':
            break
        try:
            price = float(user_input)
            if price <= 0:
                print(color_text("Price must be positive.", 'red'))
                continue
            prices.append(price)
        except ValueError:
            print(color_text("Invalid input. Please enter a number or 'done'.", 'red'))
    return prices


def breakeven_calculator():
    """Run break-even calculator."""
    print_header("CSE Break-Even Price Calculator")
    
    calculator = BreakEvenCalculator()
    
    print("Choose an option:")
    print("  1. Calculate break-even price (minimum sell price to break even)")
    print("  2. Calculate profit/loss at a specific selling price")
    print()
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print(color_text("Invalid choice. Please enter 1 or 2.", 'red'))
    
    # Get common inputs
    buy_price = get_float_input("Enter purchase price per share (LKR): ")
    quantity = get_int_input("Enter number of shares: ")
    include_tax = input("\nInclude capital gains tax in calculation? (y/n) [y]: ").lower() != 'n'
    
    if choice == '1':
        # Calculate break-even price
        print("\nCalculating break-even price...")
        result = calculator.calculate_breakeven_price(buy_price, quantity, include_tax)
        
        # Display results
        print_section("Break-Even Analysis")
        
        data = [
            ["Purchase Price", format_currency(buy_price)],
            ["Quantity", f"{quantity:,} shares"],
            ["Total Investment", format_currency(result['total_investment'])],
            ["Buying Fees Paid", format_currency(result['buy_fees_paid'])],
            ["", ""],
            [color_text("BREAK-EVEN PRICE", 'green'), 
             color_text(format_currency(result['breakeven_price']), 'green')],
            ["", ""],
            ["Price Increase Required", format_currency(result['price_increase_required'])],
            ["Percentage Increase", format_percentage(result['price_increase_percentage'])],
            ["Includes Capital Gains Tax", "Yes" if result['includes_capital_gains_tax'] else "No"],
        ]
        
        print(tabulate(data, tablefmt="simple"))
        
        # Calculate target prices for common profit targets
        print_section("Target Prices for Profit Goals")
        
        target_data = []
        for target_pct in [10, 15, 20, 30]:
            target_result = calculator.calculate_target_price(
                buy_price, quantity, target_pct, include_tax
            )
            target_data.append([
                f"{target_pct}%",
                format_currency(target_result['target_sell_price']),
                format_currency(target_result['net_profit'])
            ])
        
        print(tabulate(target_data, 
                       headers=["Target Profit", "Required Sell Price", "Net Profit"],
                       tablefmt="grid"))
    
    else:
        # Calculate profit at specific selling price
        sell_price = get_float_input("Enter selling price per share (LKR): ")
        
        print(f"\nCalculating profit/loss for selling at {format_currency(sell_price)}...")
        result = calculator.calculate_profit_at_price(buy_price, sell_price, quantity, include_tax)
        
        # Display results
        print_section("Profit/Loss Analysis")
        
        profit_color = 'green' if result['net_profit'] > 0 else 'red' if result['net_profit'] < 0 else 'yellow'
        status_text = "PROFIT" if result['net_profit'] > 0 else "LOSS" if result['net_profit'] < 0 else "BREAK-EVEN"
        
        data = [
            ["Purchase Price", format_currency(buy_price)],
            ["Selling Price", format_currency(sell_price)],
            ["Quantity", f"{quantity:,} shares"],
            ["Price Change", format_currency(sell_price - buy_price)],
            ["Percentage Change", format_percentage((sell_price - buy_price) / buy_price)],
            ["", ""],
            ["Total Investment", format_currency(result['total_investment'])],
            ["Total Fees Paid", format_currency(result['total_fees'])],
            ["Gross Profit/Loss", format_currency(result['gross_profit'])],
            ["Capital Gains Tax", format_currency(result['capital_gains_tax'])],
            ["", ""],
            [color_text("NET PROFIT/LOSS", profit_color), 
             color_text(format_currency(result['net_profit']), profit_color)],
            ["Profit/Loss Percentage", color_text(format_percentage(result['profit_percentage']), profit_color)],
            ["Status", color_text(status_text, profit_color)],
            ["", ""],
            ["Break-Even Price", format_currency(result['breakeven_price'])],
            ["Above/Below Break-Even", 
             color_text(format_currency(result['price_vs_breakeven']), 
                       'green' if result['above_breakeven'] else 'red')],
        ]
        
        print(tabulate(data, tablefmt="simple"))
        
        # Additional insights
        if result['above_breakeven']:
            print_section("💡 Insights")
            if result['profit_percentage'] >= 20:
                print(color_text("🎉 Excellent profit! Consider taking some profits.", 'green'))
            elif result['profit_percentage'] >= 10:
                print(color_text("👍 Good profit. Hold or consider partial profit-taking.", 'green'))
            else:
                print(color_text("✅ Small profit above break-even. Monitor for better opportunities.", 'yellow'))
        else:
            loss_pct = abs(result['profit_percentage'])
            print_section("⚠️  Insights")
            if loss_pct >= 20:
                print(color_text("🚨 Significant loss. Consider cutting losses or waiting for recovery.", 'red'))
            elif loss_pct >= 10:
                print(color_text("⚠️ Moderate loss. Evaluate if fundamentals support holding.", 'red'))
            else:
                print(color_text("📉 Small loss, close to break-even. Consider holding if bullish.", 'yellow'))
            
            to_breakeven = result['breakeven_price'] - sell_price
            print(color_text(f"Need price increase of {format_currency(to_breakeven)} ({format_percentage((to_breakeven/sell_price)*100)}) to break even.", 'blue'))


def fundamental_analysis():
    """Run fundamental analysis."""
    print_header("CSE Fundamental Analysis")
    
    analyzer = FundamentalAnalyzer()
    
    print("Enter financial data for the stock:\n")
    
    # Get basic data
    stock_data = {}
    stock_data['ticker'] = input("Stock ticker/symbol (optional): ") or None
    stock_data['price'] = get_float_input("Current market price (LKR): ")
    stock_data['eps'] = get_float_input("Earnings per share (EPS): ", allow_zero=True)
    stock_data['book_value_per_share'] = get_float_input("Book value per share: ")
    stock_data['net_income'] = get_float_input("Annual net income: ", allow_zero=True)
    stock_data['shareholders_equity'] = get_float_input("Shareholders' equity: ")
    stock_data['total_debt'] = get_float_input("Total debt/liabilities: ", allow_zero=True)
    stock_data['current_assets'] = get_float_input("Current assets: ")
    stock_data['current_liabilities'] = get_float_input("Current liabilities: ")
    
    # Optional data
    prev_eps = input("\nPrevious year EPS (optional, press Enter to skip): ")
    if prev_eps:
        stock_data['previous_eps'] = float(prev_eps)
    
    annual_div = input("Annual dividend per share (optional, press Enter to skip): ")
    if annual_div:
        stock_data['annual_dividend'] = float(annual_div)
    
    # Perform analysis
    result = analyzer.comprehensive_analysis(stock_data)
    
    # Display results
    print_section("Fundamental Analysis Results")
    
    metrics_data = []
    for metric_name, metric_data in result['metrics'].items():
        if isinstance(metric_data, dict):
            value = metric_data.get('pe_ratio') or metric_data.get('pb_ratio') or \
                    metric_data.get('roe_percentage') or metric_data.get('debt_to_equity_ratio') or \
                    metric_data.get('current_ratio') or metric_data.get('growth_percentage') or \
                    metric_data.get('yield_percentage')
            
            score = metric_data.get('score', 0)
            recommendation = metric_data.get('recommendation', 'N/A')
            
            # Color code based on score
            if score >= 75:
                score_color = 'green'
            elif score >= 50:
                score_color = 'yellow'
            else:
                score_color = 'red'
            
            metrics_data.append([
                metric_name.upper().replace('_', ' '),
                value if value is not None else 'N/A',
                color_text(f"{score}/100", score_color),
                recommendation
            ])
    
    print(tabulate(metrics_data, 
                   headers=["Metric", "Value", "Score", "Assessment"],
                   tablefmt="grid"))
    
    # Overall summary
    print_section("Overall Assessment")
    
    score = result['overall_score']
    if score >= 75:
        score_color = 'green'
    elif score >= 60:
        score_color = 'yellow'
    else:
        score_color = 'red'
    
    summary_data = [
        ["Overall Score", color_text(f"{score}/100", score_color)],
        ["Recommendation", color_text(result['overall_recommendation'], score_color)],
        ["Metrics Analyzed", result['metrics_analyzed']]
    ]
    
    print(tabulate(summary_data, tablefmt="simple"))


def full_stock_analysis():
    """Run complete stock analysis with recommendations."""
    print_header("CSE Complete Stock Analysis")
    
    engine = RecommendationEngine()
    
    print("This tool provides comprehensive analysis combining fundamental,")
    print("technical, and risk assessment for investment decisions.\n")
    
    # Get fundamental data
    print_section("Step 1: Fundamental Data")
    
    stock_data = {}
    stock_data['ticker'] = input("Stock ticker/symbol: ")
    stock_data['company_name'] = input("Company name (optional): ") or None
    stock_data['price'] = get_float_input("Current market price (LKR): ")
    stock_data['eps'] = get_float_input("Earnings per share (EPS): ", allow_zero=True)
    stock_data['book_value_per_share'] = get_float_input("Book value per share: ")
    stock_data['net_income'] = get_float_input("Annual net income: ", allow_zero=True)
    stock_data['shareholders_equity'] = get_float_input("Shareholders' equity: ")
    stock_data['total_debt'] = get_float_input("Total debt: ", allow_zero=True)
    stock_data['current_assets'] = get_float_input("Current assets: ")
    stock_data['current_liabilities'] = get_float_input("Current liabilities: ")
    
    # Get historical prices for technical analysis
    print_section("Step 2: Historical Prices (for Technical Analysis)")
    
    include_technical = input("\nInclude technical analysis? (y/n) [y]: ").lower() != 'n'
    prices = None
    
    if include_technical:
        print("\nYou need at least 15 historical daily closing prices for technical analysis.")
        print("For best results, provide 50-200 historical prices.\n")
        prices = get_price_list()
        
        if len(prices) < 15:
            print(color_text(f"\nWarning: Only {len(prices)} prices provided. "
                           "Technical analysis will be limited.", 'yellow'))
    
    # Generate recommendation
    print("\n" + color_text("Analyzing... Please wait.", 'cyan'))
    
    recommendation = engine.generate_recommendation(stock_data, prices)
    
    # Display results
    print_section("Analysis Results")
    
    # Stock info
    if recommendation['stock_info']:
        info = recommendation['stock_info']
        print(color_text(f"\n{info.get('ticker', 'N/A')}", 'cyan') + 
              (f" - {info.get('company_name', '')}" if info.get('company_name') else ""))
        print(f"Current Price: {format_currency(info.get('current_price', 0))}\n")
    
    # Overall recommendation
    rec = recommendation['recommendation']
    score = recommendation['overall_score']
    
    if 'STRONG BUY' in rec:
        rec_color = 'green'
    elif 'BUY' in rec:
        rec_color = 'green'
    elif 'HOLD' in rec:
        rec_color = 'yellow'
    else:
        rec_color = 'red'
    
    print(color_text(f"RECOMMENDATION: {rec}", rec_color))
    print(color_text(f"Overall Score: {score}/100", rec_color))
    print(f"Confidence Level: {recommendation['confidence']}\n")
    
    # Scores breakdown
    scores_data = [
        ["Fundamental Score", 
         f"{recommendation['fundamental_analysis']['overall_score']}/100"],
        ["Technical Score", 
         f"{recommendation['technical_analysis']['overall_score']}/100"],
        ["Risk Score", 
         f"{recommendation['risk_assessment']['risk_score']}/100"],
        ["", ""],
        ["OVERALL SCORE", color_text(f"{score}/100", rec_color)]
    ]
    
    print(tabulate(scores_data, tablefmt="simple"))
    
    # Key strengths
    if recommendation['key_strengths']:
        print_section("Key Strengths")
        for i, strength in enumerate(recommendation['key_strengths'], 1):
            print(color_text(f"  ✓ {strength}", 'green'))
    
    # Key concerns
    if recommendation['key_concerns']:
        print_section("Key Concerns")
        for i, concern in enumerate(recommendation['key_concerns'], 1):
            print(color_text(f"  ✗ {concern}", 'red'))
    
    # Action items
    if recommendation['action_items']:
        print_section("Recommended Actions")
        for i, action in enumerate(recommendation['action_items'], 1):
            print(f"  {i}. {action}")


def display_menu():
    """Display main menu."""
    print_header("CSE Stock Analysis & Break-Even Calculator")
    
    print("Select an option:\n")
    print("  1. Break-Even Price Calculator")
    print("  2. Fundamental Analysis")
    print("  3. Complete Stock Analysis (with Recommendations)")
    print("  4. View CSE Fee Structure")
    print("  5. Exit")
    print()


def show_fee_structure():
    """Display CSE fee structure."""
    print_header("Colombo Stock Exchange (CSE) Fee Structure")
    
    calculator = CSEFeeCalculator()
    fees = calculator.get_fee_summary()
    
    print_section("Tier 1: Transactions up to Rs. 100Mn")
    tier1_data = [
        ["Brokerage Fees", fees['tier_1_brokerage']],
        ["CSE Fees", fees['tier_1_cse']],
        ["CDS Fees", fees['tier_1_cds']],
        ["SEC Fees", fees['tier_1_sec']],
        ["Share Transaction Levy", fees['tier_1_stl']],
        ["", ""],
        ["Total (excluding STL)", fees['tier_1_total']],
    ]
    
    print(tabulate(tier1_data, tablefmt="simple"))
    
    print_section("Tier 2: Transactions over Rs. 100Mn")
    tier2_data = [
        ["Minimum Brokerage", fees['tier_2_brokerage']],
        ["CSE Fees", fees['tier_2_cse']],
        ["CDS Fees", fees['tier_2_cds']],
        ["SEC Fees", fees['tier_2_sec']],
        ["Share Transaction Levy", fees['tier_2_stl']],
    ]
    
    print(tabulate(tier2_data, tablefmt="simple"))
    
    print_section("Additional Information")
    additional_data = [
        ["Capital Gains Tax", fees['capital_gains_tax']],
        ["Minimum Commission", fees['minimum_commission']],
        ["", ""],
        ["Round-trip cost (Tier 1)", "~1.42% (including STL)"],
        ["Round-trip cost (Tier 2)", "~0.66% (including STL)"],
    ]
    
    print(tabulate(additional_data, tablefmt="simple"))
    
    print("\nNote: Share Transaction Levy (0.3%) is only charged on sell transactions.")
    print("Round-trip cost includes buy fees + sell fees (including STL) + capital gains tax.")


def main():
    """Main application entry point."""
    setup_logging(log_file_prefix="cse_cli")
    logger.info("Starting CSE Stock Analyzer CLI")
    
    try:
        while True:
            display_menu()
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                breakeven_calculator()
            elif choice == '2':
                fundamental_analysis()
            elif choice == '3':
                full_stock_analysis()
            elif choice == '4':
                show_fee_structure()
            elif choice == '5':
                print("\n" + color_text("Thank you for using CSE Stock Analyzer!", 'cyan'))
                print("Good luck with your investments!\n")
                sys.exit(0)
            else:
                print(color_text("\nInvalid choice. Please select 1-5.", 'red'))
            
            input("\nPress Enter to continue...")
            print("\n" * 2)
    
    except KeyboardInterrupt:
        print("\n\n" + color_text("Program interrupted by user.", 'yellow'))
        logger.info("Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception("An unhandled error occurred")
        print(color_text(f"\nAn error occurred: {str(e)}", 'red'))
        sys.exit(1)


if __name__ == "__main__":
    main()
