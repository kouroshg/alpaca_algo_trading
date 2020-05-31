import alpaca_trade_api as tradeapi
import json
import os

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

key = os.getenv('ALPACA_KEY')
secret = os.getenv('ALPACA_SECRET')
endpoint = os.getenv('ALPACA_PAPER_BASE_URL')

api = tradeapi.REST(key, secret, base_url=endpoint, api_version='v2')

def get_account():
    return api.get_account()

def get_next_open():
    return datetime.timestamp(api.get_clock().next_open)

def get_next_close():
    return datetime.timestamp(api.get_clock().next_close)

def is_market_open():
    return api.get_clock().is_open

def cleanup_json(jsonStr):
    cleaned = str(jsonStr).replace("Bar(","").replace(")","").replace("'","\"")
    return json.loads(cleaned)

def get_bars(symbols, timeframe, count):
    bars = api.get_barset(symbols, timeframe, limit=count)
    bars = cleanup_json(bars)
    return bars