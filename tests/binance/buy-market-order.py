# Manage PATH importation of src/binance/client
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
market_operation = 'BUY'
amount_USDT = 1

BinanceClient.get_current_price(study_pair)

to_buy = 20

BinanceClient.place_market_order(study_pair, to_buy, market_operation)
