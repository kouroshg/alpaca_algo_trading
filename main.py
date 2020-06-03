import json, time, math, numpy

from tabulate import tabulate
from datetime import datetime

import alpaca, market, money

max_trade_count = 2
available_fund = 1000
timeframe = "1D"

money = money.manage(available_fund, max_trade_count)
api = alpaca.api
now = datetime.timestamp(datetime.now())

# Yahoo Finance: Gainers and Trending
print('Getting gainers and trending symbols...')
movers = list(set().union(market.getGainers(), market.getTrending()))
print('Check for symbols availability')
symbols = [sym for sym in movers if alpaca.get_asset(sym) != None]
# [print(alpaca.get_asset(sym)) for sym in movers]
def generate_table():
    # bars = alpaca.get_bars(symbols,timeframe,1)
    quotes = market.getQuote(','.join(symbols))
    table = []
    for sym in symbols:
        if len(quotes) == 0:
            continue
        try:
            last_close = quotes[sym]['prev_close']
            regular_open = quotes[sym]['open']
            qty = money.get_num_of_shares(regular_open)
            cost = qty * regular_open
            gap = regular_open - last_close
            table.append([sym, regular_open , gap, qty, cost, last_close])
        except:
            print("Error getting quote for Symbol: " + sym)
            continue

    headers = ["Symbol", "Current", "Gap", "Shares", "Cost", "Last close"]
    sorted_table = sorted(table,key=lambda x: x[2])
    print(tabulate(sorted_table,headers=headers))
    return sorted_table

table = generate_table()

def get_buying_assets():
    buying = []
    if len(api.list_positions()) == 0:
        for asset in table[0:max_trade_count]:
            gap = asset[2]
            sym = asset[0]
            qty = asset[3]
            if gap < 0:
                print("Buying {0} shares of {1}".format(qty,sym))
                buying.append(asset)
    return buying

buying = get_buying_assets()

if len(buying) > 0:
    confirm = input ("Submit order? [y/n]")
    if confirm == "y":
        for i in range (0,len(buying)):
            api.submit_order(buying[i][0],buying[i][3],"buy","market","gtc")


[print(p.side + " " + p.symbol + " p/l: " + p.unrealized_pl) for p in api.list_positions()]
confirm = input("Close all? [y/n]")
if confirm == "y":
    api.close_all_positions()
    print("Positions closed")

# The End!