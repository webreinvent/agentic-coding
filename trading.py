#!/usr/bin/env python3
"""
Real-time Trading Alert System

This script monitors real-time 1-minute bars for a configurable watchlist of symbols,
computes technical indicators (SuperTrend and RSI), and sends alerts when specific
conditions are met.

Dependencies:
- pandas: `pip install pandas`
- pandas_ta: `pip install pandas_ta`
- numpy: `pip install numpy`
- colorama: `pip install colorama` (for colored console output)

For real market data, you would need:
- windsurf: `pip install windsurf`

For testing, this script can use the included mock_windsurf.py module.

Usage:
    python trading.py
"""

import os
import sys
import time
import logging
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional

import pandas as pd
import pandas_ta as ta
import numpy as np

# Import colorama for colored console output
try:
    from colorama import init, Fore, Style
    # Initialize colorama
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    # If colorama is not available, define dummy color constants
    class DummyFore:
        RED = ""
        GREEN = ""
        RESET = ""
    
    class DummyStyle:
        RESET_ALL = ""
    
    Fore = DummyFore()
    Style = DummyStyle()
    COLOR_ENABLED = False
    print("For colored output, install colorama: pip install colorama")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Configuration
WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Symbols to monitor
CHECK_INTERVAL = 60  # Seconds between checks (1 minute)
SUPER_LEN = 10  # SuperTrend length
SUPER_MULT = 3.0  # SuperTrend multiplier
RSI_LEN = 14  # RSI length

# Email configuration
EMAIL_ENABLED = False  # Set to True to enable email alerts
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASS = "your-app-password"  # Use app password for Gmail
EMAIL_FROM = "your-email@gmail.com"
EMAIL_TO = "recipient@example.com"

# Constants
MINUTES_IN_DAY = 24 * 60
MAX_BARS = MINUTES_IN_DAY  # Store one day's worth of 1-minute bars


class BarData:
    """Class to store and process bar data for a symbol."""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bars = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        self.last_alert_time = None
    
    def add_bar(self, bar: Dict) -> None:
        """Add a new bar to the dataframe and maintain the rolling window."""
        new_bar = pd.DataFrame([{
            'timestamp': bar['timestamp'],
            'open': bar['open'],
            'high': bar['high'],
            'low': bar['low'],
            'close': bar['close'],
            'volume': bar['volume']
        }])
        
        self.bars = pd.concat([self.bars, new_bar], ignore_index=True)
        
        # Keep only the last MAX_BARS
        if len(self.bars) > MAX_BARS:
            self.bars = self.bars.iloc[-MAX_BARS:]
    
    def calculate_indicators(self) -> Dict:
        """Calculate SuperTrend and RSI indicators."""
        if len(self.bars) < max(SUPER_LEN, RSI_LEN) + 1:
            return {'supertrend_direction': 0, 'rsi': 0.0}
        
        # Calculate SuperTrend
        supertrend = ta.supertrend(
            high=self.bars['high'],
            low=self.bars['low'],
            close=self.bars['close'],
            length=SUPER_LEN,
            multiplier=SUPER_MULT
        )
        
        # Extract SuperTrend direction (1 for bullish, -1 for bearish)
        if supertrend is not None and not supertrend.empty:
            direction_col = f'SUPERTd_{SUPER_LEN}_{SUPER_MULT}'
            supertrend_direction = supertrend[direction_col].iloc[-1]
        else:
            supertrend_direction = 0
        
        # Calculate RSI
        rsi = ta.rsi(self.bars['close'], length=RSI_LEN)
        current_rsi = rsi.iloc[-1] if rsi is not None and len(rsi) > 0 else 0.0
        
        return {
            'supertrend_direction': supertrend_direction,
            'rsi': current_rsi
        }
    
    def check_alert_conditions(self) -> bool:
        """Check if alert conditions are met."""
        indicators = self.calculate_indicators()
        
        # Check conditions: SuperTrend is bullish (1) and RSI > 50
        is_bullish = indicators['supertrend_direction'] == 1
        is_rsi_strong = indicators['rsi'] > 50
        
        return is_bullish and is_rsi_strong


class WindsurfClient:
    """Client to interact with the windsurf library."""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.bar_data = {symbol: BarData(symbol) for symbol in symbols}
        self.client = None
        self.subscriptions = {}
    
    def connect(self) -> bool:
        """Connect to the windsurf client."""
        try:
            # First try to import the real windsurf library
            try:
                import windsurf
                self.client = windsurf.Client()
                logger.info("Connected to windsurf client")
                return True
            except ImportError:
                # If real windsurf is not available, try to use our mock implementation
                logger.warning("Real windsurf library not found. Falling back to mock implementation.")
                try:
                    import mock_windsurf as windsurf
                    self.client = windsurf.Client()
                    logger.info("Connected to mock windsurf client")
                    return True
                except ImportError:
                    logger.error("Failed to import windsurf or mock_windsurf. Please ensure one is available.")
                    return False
        except Exception as e:
            logger.error(f"Failed to connect to windsurf client: {e}")
            return False
    
    def subscribe(self) -> bool:
        """Subscribe to 1-minute bars for all symbols."""
        if not self.client:
            logger.error("Client not connected")
            return False
        
        try:
            for symbol in self.symbols:
                # Subscribe to 1-minute bars
                subscription = self.client.subscribe_bars(
                    symbol=symbol,
                    interval="1m",
                    callback=self._on_bar
                )
                self.subscriptions[symbol] = subscription
                logger.info(f"Subscribed to 1-minute bars for {symbol}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to bars: {e}")
            return False
    
    def _on_bar(self, bar: Dict) -> None:
        """Callback function for new bars."""
        symbol = bar.get('symbol')
        if symbol not in self.bar_data:
            return
        
        # Add the new bar to our data
        self.bar_data[symbol].add_bar(bar)
        
        # Calculate indicators
        indicators = self.bar_data[symbol].calculate_indicators()
        
        # Determine color for SuperTrend direction
        if indicators['supertrend_direction'] == 1:
            supertrend_text = f"{Fore.GREEN}Bullish{Style.RESET_ALL}" if COLOR_ENABLED else "Bullish"
        else:
            supertrend_text = f"{Fore.RED}Bearish{Style.RESET_ALL}" if COLOR_ENABLED else "Bearish"
        
        # Log bar information
        logger.info(
            f"{symbol} - Close: {bar['close']:.2f}, "
            f"RSI: {indicators['rsi']:.2f}, "
            f"SuperTrend: {supertrend_text}"
        )
        
        # Check alert conditions
        if self.bar_data[symbol].check_alert_conditions():
            self._handle_alert(symbol, bar, indicators)
    
    def _handle_alert(self, symbol: str, bar: Dict, indicators: Dict) -> None:
        """Handle alert when conditions are met."""
        # Prevent alert spam by checking last alert time
        current_time = datetime.datetime.now()
        last_alert = self.bar_data[symbol].last_alert_time
        
        # Only alert once per hour for the same symbol
        if last_alert and (current_time - last_alert).total_seconds() < 3600:
            return
        
        self.bar_data[symbol].last_alert_time = current_time
        
        alert_msg = (
            f"ALERT: {symbol} meets trading criteria!\n"
            f"Time: {bar['timestamp']}\n"
            f"Price: {bar['close']:.2f}\n"
            f"RSI: {indicators['rsi']:.2f}\n"
            f"SuperTrend: Bullish\n"
        )
        
        logger.info(alert_msg)
        
        if EMAIL_ENABLED:
            self._send_email_alert(symbol, alert_msg)
    
    def _send_email_alert(self, symbol: str, message: str) -> None:
        """Send email alert."""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM
            msg['To'] = EMAIL_TO
            msg['Subject'] = f"Trading Alert: {symbol}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent for {symbol}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    def disconnect(self) -> None:
        """Disconnect from the windsurf client."""
        try:
            if self.client:
                # Unsubscribe from all subscriptions
                for symbol, subscription in self.subscriptions.items():
                    subscription.unsubscribe()
                
                # Close the client
                self.client.close()
                logger.info("Disconnected from windsurf client")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")


def main():
    """Main function to run the trading alert system."""
    logger.info("Starting Trading Alert System")
    logger.info(f"Monitoring symbols: {', '.join(WATCHLIST)}")
    logger.info(f"SuperTrend parameters: Length={SUPER_LEN}, Multiplier={SUPER_MULT}")
    logger.info(f"RSI Length: {RSI_LEN}")
    logger.info(f"Email alerts: {'Enabled' if EMAIL_ENABLED else 'Disabled'}")
    
    client = WindsurfClient(WATCHLIST)
    
    try:
        # Connect to windsurf
        if not client.connect():
            logger.error("Failed to connect. Exiting.")
            return
        
        # Subscribe to bars
        if not client.subscribe():
            logger.error("Failed to subscribe to bars. Exiting.")
            client.disconnect()
            return
        
        # Main loop
        logger.info("Monitoring started. Press Ctrl+C to exit.")
        while True:
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        client.disconnect()
        logger.info("Trading Alert System stopped")


if __name__ == "__main__":
    main()