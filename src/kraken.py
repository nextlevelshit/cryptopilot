# Module that provides an interface for the Kraken API.

import krakenex
import time

class KrakenAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api = krakenex.API(api_key, api_secret)

    def get_recent_ohlc_data(self, pair, interval):
        """
        Retrieves recent OHLC data from the Kraken API.

        :param pair: trading pair to retrieve data for (e.g. 'XBTUSD')
        :param interval: time interval in minutes (e.g. 15)
        :return: list of OHLC data points
        """
        ohlc_data = self.api.query_public("OHLC", {"pair": pair, "interval": interval})["result"][pair]
        return [(int(t), float(o), float(h), float(l), float(c), float(vw), int(vol), int(ct)) for t, o, h, l, c, vw, vol, ct in ohlc_data]

    def get_account_balance(self):
        """
        Retrieves the account balance from the Kraken API.

        :return: dictionary of account balances
        """
        return self.api.query_private("Balance")["result"]

    def place_market_order(self, pair, side, volume):
        """
        Places a market order with the Kraken API.

        :param pair: trading pair to place order for (e.g. 'XBTUSD')
        :param side: side of the order ('buy' or 'sell')
        :param volume: volume of the order
        :return: dictionary of order information
        """
#         return self.api.query_private("AddOrder", {"pair": pair, "type": side, "ordertype": "market", "volume": volume})

    def get_open_orders(self, pair):
        """
        Retrieves a list of open orders for the given trading pair.

        :param pair: trading pair to retrieve open orders for (e.g. 'XBTUSD')
        :return: list of open orders
        """
        return []

    def get_open_positions(self):
        return []
#         return self.api.query_private("OpenOrders", {"pair": pair})["result"]["open"]

    def cancel_order(self, order_id):
        """
        Cancels the specified order.

        :param order_id: ID of the order to cancel
        :return: dictionary containing information about the cancelled order
        """
        print("CancelOrder", {"txid": order_id})
        return self.api.query_private("CancelOrder", {"txid": order_id})

    def get_ohlc_data(self, pair, interval, since=None):
        """
        Retrieves OHLC data from the Kraken API.

        :param pair: trading pair to retrieve data for (e.g. 'XBTUSD')
        :param interval: time interval in minutes (e.g. 15)
        :param since: return committed OHLC data since given id (optional)
        :return: list of OHLC data points
        """
        params = {"pair": pair, "interval": interval}
        if since:
            params["since"] = since
#         print(self.api.query_public("OHLC", params)["result"])
        ohlc_data = self.api.query_public("OHLC", params)["result"][pair]
        return [(float(t), float(o), float(h), float(l), float(c), float(vw), float(vol), float(ct)) for t, o, h, l, c, vw, vol, ct in ohlc_data]
