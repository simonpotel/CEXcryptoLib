import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))
sys.path.append(project_root)

from src.binance.client import BinanceClient
from src.json import load_json_config

keys_config = load_json_config('configs/keys.json')['Binance']

BinanceClient = BinanceClient(keys_config['api_key'], keys_config['api_secret'])

study_pair = 'DOGEUSDT'
asset = 'DOGE'
market_operation = 'SELL'
amount_DOGE = float(BinanceClient.get_balance(asset)['free'])
available_SELL = BinanceClient.get_max_sell_amount(asset, study_pair)
BinanceClient.place_market_order(study_pair, available_SELL, market_operation)

