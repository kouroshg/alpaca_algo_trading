import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url_movers = os.getenv('YAHOO_FINANCE_MOVERS')
url_trending = os.getenv('YAHOO_FINANCE_TRENDING')
host = os.getenv('RAPIDAPI_HOST')
key = os.getenv('RAPIDAPI_KEY')

querystring = {"region":"US","lang":"en"}

headers = {
    'x-rapidapi-host': host,
    'x-rapidapi-key': key
    }

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