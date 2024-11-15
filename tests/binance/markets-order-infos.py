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

asset = 'DOGE'
pair = 'DOGEUSDT'
asset_amount = 19.8

BinanceClient.simulate_trade(asset, pair, asset_amount=asset_amount, trade_type='SELL')
