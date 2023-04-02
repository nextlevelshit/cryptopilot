# Module that contains the trading strategy.

import numpy as np
import talib
import time
from cryptopilot import kraken, config

def calculate_fibonacci_levels(high, low, levels):
    """
    Calculates the Fibonacci retracement levels for the given price range.

    :param high: array of high prices
    :param low: array of low prices
    :param levels: list of Fibonacci levels to calculate
    :return: dictionary of Fibonacci levels and their corresponding prices
    """
    price_range = max(high) - min(low)
    levels = np.array(levels)
    fib_levels = {}
    for level in levels:
        fib_levels[level] = min(low) + price_range * level
    return fib_levels


def execute_trades(ohlc_data, upper_band, middle_band, lower_band, fib_levels, kraken_api):
    """
    Executes trades based on the given indicators and trading rules.

    :param ohlc_data: list of OHLC data points
    :param upper_band: array of upper Bollinger Band values
    :param middle_band: array of middle Bollinger Band values
    :param lower_band: array of lower Bollinger Band values
    :param fib_levels: dictionary of Fibonacci levels and their corresponding prices
    :param kraken_api: KrakenAPI object for executing trades
    """

    # Retrieve account balance
    account_balance = kraken_api.get_account_balance()
    print(f"Account balance: {account_balance}")

    # Check for existing open orders
    open_orders = kraken_api.get_open_orders(config.PAIR)
    if open_orders:
        print(f"Open orders: {open_orders}")
        for order in open_orders:
            kraken_api.cancel_order(order["txid"])
        print("Cancelled open orders.")

    # Execute trades
    last_price = ohlc_data[-1][4]
    for i in range(config.LOOKBACK_PERIOD, len(ohlc_data)):
        current_price = ohlc_data[i][4]

        # Check for sell signal
        if current_price >= fib_levels[0.618] and last_price < fib_levels[0.618] and \
                upper_band[i] >= current_price >= middle_band[i] and \
                lower_band[i] < last_price < middle_band[i]:
            print(f"Sell signal detected at {current_price:.4f}.")
#             kraken_api.sell(config.PAIR, config.TRADE_SIZE)
            print(f"Sold {config.TRADE_SIZE} {config.CURRENCY} at {current_price:.4f}.")

        # Check for buy signal
        if current_price <= fib_levels[0.382] and last_price > fib_levels[0.382] and \
                lower_band[i] <= current_price <= middle_band[i] and \
                upper_band[i] > last_price > middle_band[i]:
            print(f"Buy signal detected at {current_price:.4f}.")
#             kraken_api.buy(config.PAIR, config.TRADE_SIZE)
            print(f"Bought {config.TRADE_SIZE} {config.CURRENCY} at {current_price:.4f}.")

        last_price = current_price


    # Close any open positions
    open_positions = kraken_api.get_open_positions()
    if open_positions:
        print(f"Open positions: {open_positions}")
        for position in open_positions:
            if position["type"] == "sell":
#                 kraken_api.buy(config.PAIR, position["volume"])
                print(f"Bought {position['volume']} {config.CURRENCY} to close short position at {current_price:.4f}.")
            elif position["type"] == "buy":
#                 kraken_api.sell(config.PAIR, position["volume"])
                print(f"Sold {position['volume']} {config.CURRENCY} to close long position at {current_price:.4f}.")
        print("Closed open positions.")

    # Print final account balance
    account_balance = kraken_api.get_account_balance()
    print(f"Final account balance: {account_balance}")


def run_strategy():
    # Connect to Kraken API
    kraken_api = kraken.KrakenAPI(config.API_KEY, config.API_SECRET)

    # Retrieve OHLC data
    ohlc_data = kraken_api.get_ohlc_data(config.PAIR, config.INTERVAL, config.LOOKBACK_PERIOD)

    # Calculate Bollinger Bands
    close_data = np.array([data[4] for data in ohlc_data])
    upper_band, middle_band, lower_band = talib.BBANDS(close_data, timeperiod=config.BBANDS_PERIOD, nbdevup=config.BBANDS_DEV_UP, nbdevdn=config.BBANDS_DEV_DOWN)

    # Calculate Fibonacci levels
    high_data = np.array([data[2] for data in ohlc_data])
    low_data = np.array([data[3] for data in ohlc_data])
    fib_levels = calculate_fibonacci_levels(high_data, low_data, config.FIB_LEVELS)

    # Execute trades
    execute_trades(ohlc_data, upper_band, middle_band, lower_band, fib_levels, kraken_api)


if __name__ == '__main__':
    while True:
        run_strategy()
        time.sleep(20)
