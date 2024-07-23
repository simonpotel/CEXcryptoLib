from loguru import logger
from binance.client import Client
from binance.enums import *

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_current_price(self, pair):
        try:
            ticker = self.client.get_symbol_ticker(symbol=pair)
            price = float(ticker['price'])
            logger.info(f"Current price for {pair}: {price}")
            return price
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None

    def calculate_order(self, pair, amount, order_type='BUY'):
        price = self.get_current_price(pair)
        if price is None:
            return None
        
        if order_type == 'BUY':
            quantity = amount / price
            logger.info(f"With {amount} USDT, you can buy {quantity} {pair}.")
            return quantity
        elif order_type == 'SELL':
            proceeds = amount * price
            logger.info(f"By selling {amount} {pair}, you can get {proceeds} USDT.")
            return proceeds
        else:
            logger.error("Unsupported order type. Use 'BUY' or 'SELL'.")
            return None

    def get_trade_fee(self, pair):
        try:
            fees = self.client.get_trade_fee(symbol=pair)
            logger.info(f"Trade fee for {pair}: {fees}")
            return fees
        except Exception as e:
            logger.error(f"Error getting trade fee: {e}")
            return None

    def place_market_order(self, pair, quantity, side='BUY'):
        try:
            if side == 'BUY':
                order = self.client.order_market_buy(symbol=pair, quantity=quantity)
            elif side == 'SELL':
                order = self.client.order_market_sell(symbol=pair, quantity=quantity)
            else:
                logger.error("Unsupported order type. Use 'BUY' or 'SELL'.")
                return None
            logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            return None

    def get_all_orders(self, pair):
        try:
            orders = self.client.get_all_orders(symbol=pair)
            logger.info(f"All orders for {pair}: {orders}")
            return orders
        except Exception as e:
            logger.error(f"Error getting all orders: {e}")
            return None

    def get_open_orders(self, pair):
        try:
            open_orders = self.client.get_open_orders(symbol=pair)
            logger.info(f"Open orders for {pair}: {open_orders}")
            return open_orders
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            return None

    def get_past_trades(self, pair):
        try:
            trades = self.client.get_my_trades(symbol=pair)
            logger.info(f"Trade history for {pair}: {trades}")
            return trades
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            return None

    def get_balance(self, asset):
        try:
            balance = self.client.get_asset_balance(asset=asset)
            logger.info(f"Balance for {asset}: {balance}")
            return balance
        except Exception as e:
            logger.error(f"Error getting balance for {asset}: {e}")
            return None
        
    def get_max_sell_amount(self, asset, pair):
        try:
            # Get the available balance of the asset
            balance = self.client.get_asset_balance(asset=asset)
            available_balance = float(balance['free'])
            logger.info(f"Available balance for {asset}: {available_balance}")

            # Get the trading rules for the pair
            exchange_info = self.client.get_exchange_info()
            symbol_info = next(filter(lambda x: x['symbol'] == pair, exchange_info['symbols']))
            lot_size_filter = next(filter(lambda x: x['filterType'] == 'LOT_SIZE', symbol_info['filters']))

            min_qty = float(lot_size_filter['minQty'])
            step_size = float(lot_size_filter['stepSize'])
            logger.info(f"Trading rules for {pair}: minQty={min_qty}, stepSize={step_size}")

            # Calculate the maximum sellable amount
            max_sell_amount = available_balance - (available_balance % step_size)
            if max_sell_amount < min_qty:
                logger.info(f"Max sell amount {max_sell_amount} is less than minQty {min_qty}")
                return 0

            logger.info(f"Max sell amount for {asset} on {pair}: {max_sell_amount}")
            return max_sell_amount
        except Exception as e:
            logger.error(f"Error getting max sell amount for {asset} on {pair}: {e}")
            return None