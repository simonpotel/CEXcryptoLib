# tests/binance

## pairs-infos.py

This test provides basic information about a trading pair:
- **Current Price**: Retrieves the current rate for the pair.
- **Trade Fees**: Shows the trading fees associated with the pair.
- **All Orders**: Lists all orders for the pair.
- **Open Orders**: Lists all currently open orders for the pair.
- **Past Orders**: Retrieves all past orders for the pair.

## markets-order-infos.py

This test determines the maximum amount of an asset you can trade and calculates the fee for buying or selling the asset at the market price. For example, if you have 19.8 DOGE on Binance, this method will:
- Provide the maximum amount of DOGE you can sell, considering trading rules.
- Calculate the fee you will incur for buying or selling the asset.

Example output:
```python
(for 19.8 DOGE)

2024-07-23 22:52:50.126 | INFO     | src.binance.client:simulate_trade:133 - Trading rules for DOGEUSDT: minQty=1.0, stepSize=1.0
2024-07-23 22:52:50.419 | INFO     | src.binance.client:simulate_trade:139 - Trade fees for DOGEUSDT: Maker fee=0.001%, Taker fee=0.001%
2024-07-23 22:52:50.419 | INFO     | src.binance.client:simulate_trade:164 - Max tradable amount for SELL DOGE: 19.0
2024-07-23 22:52:50.419 | INFO     | src.binance.client:simulate_trade:165 - Fee for SELL 19.0 DOGE: 0.00019
{'max_trade_amount': 19.0, 'fee': 0.00019}
```

## buy-market-order.py

This test script attempts to buy the maximum amount of a specified asset using a given amount of USDT at market price. It simulates placing a market order and provides details about the trade.

Example output:
```python
2024-07-23 22:32:20.983 | INFO     | src.binance.client:get_current_price:13 - Current price for DOGEUSDT: [REDACTED]
2024-07-23 22:32:21.468 | INFO     | src.binance.client:place_market_order:54 - Market order placed: {'symbol': 'DOGEUSDT', 'orderId': [REDACTED], 'orderListId': [REDACTED], 'clientOrderId': [REDACTED], 'transactTime': [REDACTED], 'price': '0.00000000', 'origQty': '20.00000000', 'executedQty': '20.00000000', 'cummulativeQuoteQty': '2.61200000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'workingTime': [REDACTED], 'fills': [{'price': '0.13060000', 'qty': '20.00000000', 'commission': '0.02000000', 'commissionAsset': 'DOGE', 'tradeId': [REDACTED]}], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
```

## sell-market-order.py

This test script attempts to sell the maximum amount of a specified asset and calculates the total USDT you can obtain using a market order.




