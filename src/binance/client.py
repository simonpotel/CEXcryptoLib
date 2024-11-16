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
            symbol_info = self.client.get_symbol_info(pair)
            lot_size_filter = next(filter(lambda x: x['filterType'] == 'LOT_SIZE', symbol_info['filters']))
            
            min_qty = float(lot_size_filter['minQty'])
            step_size = float(lot_size_filter['stepSize'])
            
            adjusted_quantity = max(min_qty, (quantity // step_size) * step_size)
            
            if side == 'BUY':
                order = self.client.order_market_buy(symbol=pair, quantity=adjusted_quantity)
            elif side == 'SELL':
                order = self.client.order_market_sell(symbol=pair, quantity=adjusted_quantity)
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

    def get_symbol_info(self, symbol):
        try:
            exchange_info = self.client.get_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.info(f"Symbol info for {symbol}: {s}")
                    return s
            logger.error(f"Symbol {symbol} not found in exchange info.")
            return None
        except Exception as e:
            logger.error(f"Error getting symbol info: {e}")
            return None

    def get_max_sell_amount(self, asset, pair):
        try:
            # Get the available balance of the asset
            balance = self.client.get_asset_balance(asset=asset)
            available_balance = float(balance['free'])
            logger.info(f"Available balance for {asset}: {available_balance}")

            # Get the trading rules for the pair
            exchange_info = self.client.get_exchange_info()
            symbol_info = next(
                filter(lambda x: x['symbol'] == pair, exchange_info['symbols']))
            lot_size_filter = next(
                filter(lambda x: x['filterType'] == 'LOT_SIZE', symbol_info['filters']))

            min_qty = float(lot_size_filter['minQty'])
            step_size = float(lot_size_filter['stepSize'])
            logger.info(f"Trading rules for {pair}: minQty={min_qty}, stepSize={step_size}")

            # Calculate the maximum sellable amount
            max_sell_amount = available_balance - \
                (available_balance % step_size)
            if max_sell_amount < min_qty:
                logger.info(f"Max sell amount {max_sell_amount} is less than minQty {min_qty}")
                return 0

            logger.info(f"Max sell amount for {asset} on {pair}: {max_sell_amount}")
            return max_sell_amount
        except Exception as e:
            logger.error(f"Error getting max sell amount for {asset} on {pair}: {e}")
            return None

    def simulate_trade(self, asset, pair, asset_amount=100, trade_type='SELL'):
        try:
            # Get the trading rules for the pair
            exchange_info = self.client.get_exchange_info()
            symbol_info = next(
                filter(lambda x: x['symbol'] == pair, exchange_info['symbols']))
            lot_size_filter = next(
                filter(lambda x: x['filterType'] == 'LOT_SIZE', symbol_info['filters']))

            min_qty = float(lot_size_filter['minQty'])
            step_size = float(lot_size_filter['stepSize'])
            logger.info(f"Trading rules for {pair}: minQty={min_qty}, stepSize={step_size}")

            # Get the trade fee for the pair
            fees = self.client.get_trade_fee(symbol=pair)
            maker_fee_percent = float(fees[0]['makerCommission']) / 100
            taker_fee_percent = float(fees[0]['takerCommission']) / 100
            logger.info(f"Trade fees for {pair}: Maker fee={maker_fee_percent * 100}%, Taker fee={taker_fee_percent * 100}%")

            # Determine if it's a buy or sell
            if trade_type == 'SELL':
                # Calculate the maximum amount that can be sold
                max_trade_amount = asset_amount - (asset_amount % step_size)
            elif trade_type == 'BUY':
                # For buying, the maximum amount you can buy is also constrained by step_size
                # For simplicity, we'll assume you can use the full asset_amount
                max_trade_amount = asset_amount - (asset_amount % step_size)
            else:
                logger.error("Unsupported trade type. Use 'BUY' or 'SELL'.")
                return None

            # Calculate the fee based on the trade type
            if trade_type == 'SELL':
                fee = max_trade_amount * maker_fee_percent
            elif trade_type == 'BUY':
                fee = max_trade_amount * taker_fee_percent

            # Check if the maximum amount is below the minimum quantity
            if max_trade_amount < min_qty:
                logger.info(f"Max trade amount {max_trade_amount} is less than minQty {min_qty}")
                return None

            logger.info(f"Max tradable amount for {trade_type} {asset}: {max_trade_amount}")
            logger.info(f"Fee for {trade_type} {max_trade_amount} {asset}: {fee}")

            return {
                'max_trade_amount': max_trade_amount,
                'fee': fee
            }
        except Exception as e:
            logger.error(f"Error simulating trade for {asset} on {pair}: {e}")
            return None

    def get_max_sell_amount_with_fee(self, asset, pair, amount_to_sell):
        # didnt test
        try:
            # Get the available balance of the asset
            balance = self.client.get_asset_balance(asset=asset)
            available_balance = float(balance['free'])
            logger.info(f"Available balance for {asset}: {available_balance}")

            # Check if the amount to sell is available
            if amount_to_sell > available_balance:
                logger.error(f"Amount to sell {amount_to_sell} exceeds available balance {available_balance}")
                return None

            # Get the trading rules for the pair
            exchange_info = self.client.get_exchange_info()
            symbol_info = next(
                filter(lambda x: x['symbol'] == pair, exchange_info['symbols']))
            lot_size_filter = next(
                filter(lambda x: x['filterType'] == 'LOT_SIZE', symbol_info['filters']))

            min_qty = float(lot_size_filter['minQty'])
            step_size = float(lot_size_filter['stepSize'])
            logger.info(f"Trading rules for {pair}: minQty={min_qty}, stepSize={step_size}")

            # Get the trade fee for the pair
            fees = self.client.get_trade_fee(symbol=pair)
            trade_fee_percent = float(fees[0]['makerCommission']) / 100
            logger.info(f"Trade fee for {pair}: {trade_fee_percent * 100}%")

            # Calculate the maximum sellable amount within the given amount
            max_sell_amount = amount_to_sell - (amount_to_sell % step_size)
            if max_sell_amount < min_qty:
                logger.info(f"Max sell amount {max_sell_amount} is less than minQty {min_qty}")
                return None

            # Calculate the fee
            fee = max_sell_amount * trade_fee_percent
            logger.info(f"Fee for selling {max_sell_amount} {asset}: {fee}")

            return max_sell_amount, fee
        except Exception as e:
            logger.error(f"Error getting max sell amount and fee for {asset} on {pair}: {e}")
            return None
