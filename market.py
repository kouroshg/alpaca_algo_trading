import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url_movers = os.getenv('YAHOO_FINANCE_MOVERS')
url_trending = os.getenv('YAHOO_FINANCE_TRENDING')
url_quote = os.getenv('YAHOO_FINANCE_QUOTE')

host = os.getenv('RAPIDAPI_HOST')
key = os.getenv('RAPIDAPI_KEY')

querystring = {"region":"US","lang":"en"}

headers = {
    'x-rapidapi-host': host,
    'x-rapidapi-key': key
    }

def getQuote(symbols):
    params = querystring.copy()
    params['symbols'] = symbols
    response = requests.get(url_quote,headers=headers, params=params)
    if response.status_code == 200:
        quotes = response.json()['quoteResponse']['result']
        return {quote['symbol']:{'open':quote['regularMarketOpen'], 'prev_close':quote['regularMarketPreviousClose']} for quote in quotes}

def getGainers():
    response = requests.get(url_movers, headers=headers, params=querystring)
    if response.status_code == 200:
        gainers = response.json()['finance']['result'][0]['quotes']
        return [quote['symbol'] for quote in gainers]

def getTrending():
    response = requests.get(url_trending, headers=headers, params=querystring)
    if response.status_code == 200:
        trending = response.json()['finance']['result'][0]['quotes']
        return [quote['symbol'] for quote in trending]