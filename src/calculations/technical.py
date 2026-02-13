"""
Technical Analysis Module for Stock Trading Signals.

This module calculates technical indicators including RSI, MACD, moving averages,
and generates buy/sell signals based on technical analysis principles.
"""

import pandas as pd
import numpy as np
try:
    import pandas_ta as ta
except ImportError:
    ta = None

from src.utils.helpers import load_config
from typing import Any, Dict, List, Optional


class TechnicalAnalyzer:
    """Calculate and analyze technical indicators."""
    
    def __init__(self, custom_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize technical analyzer.
        
        Args:
            custom_config: Optional dictionary to override default config
        """
        self.config = custom_config if custom_config else load_config()
        self.thresholds = self.config['thresholds']
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> Dict[str, Any]:
        """
        Calculate Relative Strength Index (RSI).
        
        RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss over period
        
        Args:
            prices: List of historical prices (most recent last)
            period: RSI period (default: 14 days)
        
        Returns:
            dict: RSI value and interpretation
        """
        if len(prices) < period + 1:
            return {
                'rsi': None,
                'score': 50,
                'signal': 'NEUTRAL',
                'interpretation': f'Insufficient data (need at least {period + 1} prices)',
                'recommendation': 'N/A'
            }
        
        # Convert to pandas Series for easier calculation
        price_series = pd.Series(prices)
        
        # Calculate price changes
        delta = price_series.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gain = gains.rolling(window=period, min_periods=period).mean()
        avg_loss = losses.rolling(window=period, min_periods=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        rsi_series = rsi  # keep as Series for Pyre2
        current_rsi = float(rsi_series.iloc[-1])
        
        # Interpret RSI
        rsi_thresholds = self.thresholds['rsi']
        if current_rsi <= rsi_thresholds['oversold']:
            score = 90
            signal = 'STRONG BUY'
            interpretation = 'Oversold - potential buying opportunity'
            recommendation = 'BUY - Stock may be undervalued'
        elif current_rsi <= rsi_thresholds['neutral_low']:
            score = 75
            signal = 'BUY'
            interpretation = 'Below neutral - bullish territory'
            recommendation = 'Consider buying'
        elif current_rsi <= rsi_thresholds['neutral_high']:
            score = 60
            signal = 'NEUTRAL'
            interpretation = 'Neutral territory'
            recommendation = 'HOLD - Monitor for signals'
        elif current_rsi <= rsi_thresholds['overbought']:
            score = 40
            signal = 'SELL'
            interpretation = 'Above neutral - bearish territory'
            recommendation = 'Consider selling'
        else:
            score = 20
            signal = 'STRONG SELL'
            interpretation = 'Overbought - potential selling opportunity'
            recommendation = 'SELL - Stock may be overvalued'
        
        return {
            'rsi': round(float(current_rsi), 2),
            'score': score,
            'signal': signal,
            'interpretation': interpretation,
            'recommendation': recommendation
        }
    
    def calculate_macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, Any]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        MACD = 12-day EMA - 26-day EMA
        Signal Line = 9-day EMA of MACD
        Histogram = MACD - Signal Line
        
        Args:
            prices: List of historical prices (most recent last)
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line EMA period (default: 9)
        
        Returns:
            dict: MACD values and interpretation
        """
        min_required = slow + signal
        if len(prices) < min_required:
            return {
                'macd': None,
                'signal_line': None,
                'histogram': None,
                'score': 50,
                'signal': 'NEUTRAL',
                'interpretation': f'Insufficient data (need at least {min_required} prices)',
                'recommendation': 'N/A'
            }
        
        # Convert to pandas Series
        price_series = pd.Series(prices)
        
        # Calculate EMAs
        ema_fast = price_series.ewm(span=fast, adjust=False).mean()
        ema_slow = price_series.ewm(span=slow, adjust=False).mean()
        
        # Calculate MACD line
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd_line - signal_line
        
        current_macd = float(macd_line.iloc[-1])
        current_signal = float(signal_line.iloc[-1])
        current_histogram = float(histogram.iloc[-1])
        
        # Check for crossovers (if we have previous values)
        if len(histogram) > 1:
            prev_histogram = float(histogram.iloc[-2])
            
            if current_histogram > 0 and prev_histogram <= 0:
                score = 85
                signal_type = 'STRONG BUY'
                interpretation = 'Bullish crossover - MACD crossed above signal line'
                recommendation = 'BUY - Strong buy signal'
            elif current_histogram < 0 and prev_histogram >= 0:
                score = 25
                signal_type = 'STRONG SELL'
                interpretation = 'Bearish crossover - MACD crossed below signal line'
                recommendation = 'SELL - Strong sell signal'
            elif current_histogram > 0:
                score = 70
                signal_type = 'BUY'
                interpretation = 'MACD above signal line - bullish momentum'
                recommendation = 'HOLD/BUY - Positive momentum'
            else:
                score = 40
                signal_type = 'SELL'
                interpretation = 'MACD below signal line - bearish momentum'
                recommendation = 'HOLD/SELL - Negative momentum'
        else:
            if current_histogram > 0:
                score = 65
                signal_type = 'BUY'
                interpretation = 'MACD above signal line'
                recommendation = 'Positive momentum'
            else:
                score = 45
                signal_type = 'SELL'
                interpretation = 'MACD below signal line'
                recommendation = 'Negative momentum'
        
        return {
            'macd': round(float(current_macd), 4),
            'signal_line': round(float(current_signal), 4),
            'histogram': round(float(current_histogram), 4),
            'score': score,
            'signal': signal_type,
            'interpretation': interpretation,
            'recommendation': recommendation
        }
    
    def calculate_moving_averages(self, prices: List[float], short_period: int = 50, long_period: int = 200) -> Dict[str, Any]:
        """
        Calculate Simple Moving Averages and identify trends.
        
        Args:
            prices: List of historical prices (most recent last)
            short_period: Short-term MA period (default: 50)
            long_period: Long-term MA period (default: 200)
        
        Returns:
            dict: Moving averages and interpretation
        """
        current_price = prices[-1]
        
        results = {
            'current_price': current_price,
            'short_ma': None,
            'long_ma': None,
            'score': 50,
            'signal': 'NEUTRAL',
            'interpretation': '',
            'recommendation': 'N/A'
        }
        
        # Calculate short-term MA
        if len(prices) >= short_period:
            short_ma = sum(prices[-short_period:]) / short_period
            results['short_ma'] = round(float(short_ma), 2)
            
            # Compare price to short MA
            if current_price > short_ma:
                short_trend = 'above'
                short_score = 70
            else:
                short_trend = 'below'
                short_score = 40
        else:
            short_trend = None
            short_score = 50
        
        # Calculate long-term MA
        if len(prices) >= long_period:
            long_ma = sum(prices[-long_period:]) / long_period
            results['long_ma'] = round(float(long_ma), 2)
            
            # Compare price to long MA
            if current_price > long_ma:
                long_trend = 'above'
                long_score = 70
            else:
                long_trend = 'below'
                long_score = 40
        else:
            long_trend = None
            long_score = 50
        
        # Determine overall trend and signal
        if short_trend and long_trend:
            # Check for golden cross or death cross
            short_ma_val: float = results['short_ma']  # type: ignore[assignment]
            long_ma_val: float = results['long_ma']  # type: ignore[assignment]
            if short_ma_val > long_ma_val:
                # Check if it's a recent crossover (golden cross)
                if len(prices) >= long_period + 1:
                    prev_short = sum(prices[-short_period-1:-1]) / short_period
                    prev_long = sum(prices[-long_period-1:-1]) / long_period
                    
                    if prev_short <= prev_long:
                        results['score'] = 95
                        results['signal'] = 'GOLDEN CROSS'
                        results['interpretation'] = 'Golden Cross - Strong bullish signal! 50-MA crossed above 200-MA'
                        results['recommendation'] = 'STRONG BUY'
                        return results
                
                results['score'] = 80
                results['signal'] = 'BULLISH'
                results['interpretation'] = f'Bullish trend - Price and {short_period}-MA above {long_period}-MA'
                results['recommendation'] = 'BUY - Strong uptrend'
            
            elif short_ma_val < long_ma_val:
                # Check for death cross
                if len(prices) >= long_period + 1:
                    prev_short = sum(prices[-short_period-1:-1]) / short_period
                    prev_long = sum(prices[-long_period-1:-1]) / long_period
                    
                    if prev_short >= prev_long:
                        results['score'] = 15
                        results['signal'] = 'DEATH CROSS'
                        results['interpretation'] = 'Death Cross - Strong bearish signal! 50-MA crossed below 200-MA'
                        results['recommendation'] = 'STRONG SELL'
                        return results
                
                results['score'] = 30
                results['signal'] = 'BEARISH'
                results['interpretation'] = f'Bearish trend - {short_period}-MA below {long_period}-MA'
                results['recommendation'] = 'SELL - Downtrend'
        
        elif short_trend:
            # Only short-term MA available
            if short_trend == 'above':
                results['score'] = 65
                results['signal'] = 'BULLISH'
                results['interpretation'] = f'Price above {short_period}-day MA - short-term uptrend'
                results['recommendation'] = 'BUY - Positive short-term momentum'
            else:
                results['score'] = 45
                results['signal'] = 'BEARISH'
                results['interpretation'] = f'Price below {short_period}-day MA - short-term downtrend'
                results['recommendation'] = 'SELL - Negative short-term momentum'
        
        else:
            results['interpretation'] = f'Insufficient data for moving averages (need {short_period}+ prices)'
        
        return results
    
    def calculate_volume_analysis(self, prices: List[float], volumes: List[float]) -> Dict[str, Any]:
        """
        Analyze volume patterns to confirm price movements.
        
        Args:
            prices: List of historical prices
            volumes: List of corresponding trading volumes
        
        Returns:
            dict: Volume analysis and interpretation
        """
        if len(prices) != len(volumes) or len(prices) < 2:
            return {
                'average_volume': None,
                'current_volume': None,
                'volume_trend': 'N/A',
                'score': 50,
                'interpretation': 'Insufficient volume data',
                'recommendation': 'N/A'
            }
        
        current_volume = volumes[-1]
        avg_volume = sum(volumes[:-1]) / len(volumes[:-1]) if len(volumes) > 1 else current_volume
        
        # Price direction
        price_change = prices[-1] - prices[-2]
        price_direction = 'up' if price_change > 0 else 'down' if price_change < 0 else 'flat'
        
        # Volume comparison
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Interpret volume with price
        if volume_ratio > 1.5:  # High volume
            if price_direction == 'up':
                score = 85
                interpretation = 'Strong buying pressure - price rising on high volume'
                recommendation = 'BUY - Strong confirmation'
                volume_trend = 'High volume supporting uptrend'
            elif price_direction == 'down':
                score = 25
                interpretation = 'Strong selling pressure - price falling on high volume'
                recommendation = 'SELL - Strong confirmation'
                volume_trend = 'High volume supporting downtrend'
            else:
                score = 50
                interpretation = 'High volume without clear direction'
                recommendation = 'WAIT - Watch for direction'
                volume_trend = 'High volume, price indecisive'
        
        elif volume_ratio < 0.7:  # Low volume
            if price_direction == 'up':
                score = 60
                interpretation = 'Price rising but on low volume - weak conviction'
                recommendation = 'CAUTION - Uptrend not well supported'
                volume_trend = 'Low volume, weak uptrend'
            elif price_direction == 'down':
                score = 55
                interpretation = 'Price falling on low volume - weak selling'
                recommendation = 'HOLD - Downtrend not well supported'
                volume_trend = 'Low volume, weak downtrend'
            else:
                score = 50
                interpretation = 'Low volume consolidation'
                recommendation = 'WAIT - Awaiting breakout'
                volume_trend = 'Low volume, consolidating'
        
        else:  # Average volume
            if price_direction == 'up':
                score = 70
                interpretation = 'Price rising on average volume'
                recommendation = 'BUY - Normal uptrend'
                volume_trend = 'Average volume uptrend'
            elif price_direction == 'down':
                score = 40
                interpretation = 'Price falling on average volume'
                recommendation = 'SELL - Normal downtrend'
                volume_trend = 'Average volume downtrend'
            else:
                score = 50
                interpretation = 'Sideways movement on average volume'
                recommendation = 'HOLD - No clear signal'
                volume_trend = 'Average volume, range-bound'
        
        return {
            'average_volume': round(float(avg_volume), 2),
            'current_volume': current_volume,
            'volume_ratio': round(float(volume_ratio), 2),
            'volume_trend': volume_trend,
            'score': score,
            'interpretation': interpretation,
            'recommendation': recommendation
        }

    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, num_std: int = 2) -> Dict[str, Any]:
        """
        Calculate Bollinger Bands (Middle, Upper, Lower).
        
        Args:
            prices: List of historical prices (most recent last)
            period: Moving average period (default: 20)
            num_std: Number of standard deviations (default: 2)
        
        Returns:
            dict: Bands values and interpretation
        """
        if len(prices) < period:
            return {
                'upper': None,
                'middle': None,
                'lower': None,
                'score': 50,
                'signal': 'NEUTRAL',
                'interpretation': f'Insufficient data (need at least {period} prices)',
                'recommendation': 'N/A'
            }
        
        price_series = pd.Series(prices)
        
        # Calculate Middle Band (SMA)
        middle_band = price_series.rolling(window=period).mean()
        
        # Calculate Standard Deviation
        std_dev = price_series.rolling(window=period).std()
        
        # Calculate Upper and Lower Bands
        upper_band = middle_band + (std_dev * num_std)
        lower_band = middle_band - (std_dev * num_std)
        
        current_price = prices[-1]
        current_upper = float(upper_band.iloc[-1])
        current_lower = float(lower_band.iloc[-1])
        current_middle = float(middle_band.iloc[-1])
        
        # Interpretation
        bandwidth = (current_upper - current_lower) / current_middle
        
        # Determine signal based on price position relative to bands
        if current_price >= current_upper:
            score = 30
            signal = 'SELL'
            interpretation = 'Price touching/above upper band - potential overbought'
            recommendation = 'Consider taking profits'
        elif current_price <= current_lower:
            score = 80
            signal = 'BUY'
            interpretation = 'Price touching/below lower band - potential oversold'
            recommendation = 'Look for buy opportunities'
        elif current_price > current_middle:
            score = 60
            signal = 'NEUTRAL-BULLISH'
            interpretation = 'Price in upper channel'
            recommendation = 'HOLD - Uptrend'
        else:
            score = 40
            signal = 'NEUTRAL-BEARISH'
            interpretation = 'Price in lower channel'
            recommendation = 'HOLD - Downtrend'
            
        return {
            'upper': round(float(current_upper), 2),
            'middle': round(float(current_middle), 2),
            'lower': round(float(current_lower), 2),
            'bandwidth': round(float(bandwidth), 4),
            'score': score,
            'signal': signal,
            'interpretation': interpretation,
            'recommendation': recommendation
        }

    def calculate_stochastic(self, prices: List[float], high_prices: Optional[List[float]] = None, low_prices: Optional[List[float]] = None, k_period: int = 14, d_period: int = 3) -> Dict[str, Any]:
        """
        Calculate Stochastic Oscillator (%K and %D).
        
        If high/low prices not provided, estimates using close prices (less accurate).
        
        Args:
            prices: List of close prices
            high_prices: List of high prices (optional)
            low_prices: List of low prices (optional)
            k_period: Lookback period for %K (default: 14)
            d_period: Smoothing period for %D (default: 3)
            
        Returns:
            dict: Stochastic values and interpretation
        """
        if len(prices) < k_period:
            return {
                'k': None,
                'd': None,
                'score': 50,
                'signal': 'NEUTRAL',
                'interpretation': f'Insufficient data (need at least {k_period} prices)',
                'recommendation': 'N/A'
            }
            
        close_series = pd.Series(prices)
        
        # Use provided high/low or estimate from close (not ideal but functional fallback)
        if high_prices and len(high_prices) == len(prices):
            high_series = pd.Series(high_prices)
        else:
            high_series = close_series
            
        if low_prices and len(low_prices) == len(prices):
            low_series = pd.Series(low_prices)
        else:
            low_series = close_series
            
        # Calculate Lowest Low and Highest High over k_period
        lowest_low = low_series.rolling(window=k_period).min()
        highest_high = high_series.rolling(window=k_period).max()
        
        # Calculate %K
        # %K = (Current Close - Lowest Low) / (Highest High - Lowest Low) * 100
        k_percent = 100 * ((close_series - lowest_low) / (highest_high - lowest_low))
        
        # Calculate %D (3-day SMA of %K)
        d_percent = k_percent.rolling(window=d_period).mean()
        
        current_k = float(k_percent.iloc[-1])
        current_d = float(d_percent.iloc[-1])
        
        # Handle NaN values at start
        if pd.isna(current_k) or pd.isna(current_d):
             return {
                'k': None, # Keep as None or handle gracefully
                'd': None,
                'score': 50,
                'signal': 'NEUTRAL',
                'interpretation': 'Calculation pending more data', 
                'recommendation': 'N/A'
            }

        # Interpretation
        if current_k < 20 and current_d < 20:
            score = 85
            signal = 'STRONG BUY'
            interpretation = 'Oversold zone - potential reversal up'
            recommendation = 'BUY - Oversold'
        elif current_k > 80 and current_d > 80:
            score = 25
            signal = 'STRONG SELL'
            interpretation = 'Overbought zone - potential reversal down'
            recommendation = 'SELL - Overbought'
        elif current_k > current_d:
            score = 65
            signal = 'BUY'
            interpretation = '%K above %D (Bullish momentum)'
            recommendation = 'BUY/HOLD'
        else:
            score = 45
            signal = 'SELL'
            interpretation = '%K below %D (Bearish momentum)'
            recommendation = 'SELL/HOLD'
            
        return {
            'k': round(float(current_k), 2),
            'd': round(float(current_d), 2),
            'score': score,
            'signal': signal,
            'interpretation': interpretation,
            'recommendation': recommendation
        }
    
    def comprehensive_analysis(self, prices: List[float], volumes: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive technical analysis.
        
        Args:
            prices: List of historical prices (most recent last)
            volumes: Optional list of trading volumes
        
        Returns:
            dict: Complete technical analysis with overall score
        """
        results = {}
        
        # RSI
        results['rsi'] = self.calculate_rsi(prices)
        
        # MACD
        results['macd'] = self.calculate_macd(prices)
        
        # Moving Averages
        results['moving_averages'] = self.calculate_moving_averages(prices)
        
        # Volume Analysis (if provided)
        if volumes and len(volumes) == len(prices):
            results['volume'] = self.calculate_volume_analysis(prices, volumes)
            
        # Bollinger Bands
        results['bollinger'] = self.calculate_bollinger_bands(prices)
        
        # Stochastic Oscillator
        results['stochastic'] = self.calculate_stochastic(prices)
        
        # Calculate overall technical score
        scores = []
        for indicator_name, indicator_data in results.items():
            if isinstance(indicator_data, dict) and 'score' in indicator_data:
                scores.append(indicator_data['score'])
        
        if scores:
            overall_score = sum(scores) / len(scores)
        else:
            overall_score = 50
        
        # Overall technical recommendation
        if overall_score >= 80:
            overall_signal = 'STRONG BUY'
            overall_recommendation = 'Strong technical buy signals'
        elif overall_score >= 65:
            overall_signal = 'BUY'
            overall_recommendation = 'Positive technical indicators'
        elif overall_score >= 50:
            overall_signal = 'HOLD'
            overall_recommendation = 'Mixed technical signals'
        elif overall_score >= 35:
            overall_signal = 'SELL'
            overall_recommendation = 'Negative technical indicators'
        else:
            overall_signal = 'STRONG SELL'
            overall_recommendation = 'Strong technical sell signals'
        
        return {
            'indicators': results,
            'overall_score': round(float(overall_score), 2),
            'overall_signal': overall_signal,
            'overall_recommendation': overall_recommendation,
            'indicators_analyzed': len(results)
        }
