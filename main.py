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
symbols = list(set().union(market.getGainers(), market.getTrending()))

if not alpaca.is_market_open():
    print ("Waiting for market open...")
    time.sleep(alpaca.get_next_open() - now)

def generate_table():
    bars = alpaca.get_bars(symbols,timeframe,1)
    table = []
    for sym in symbols:
        if bars[sym]==None:
            continue
        if len(bars[sym]) == 0:
            continue
        try:
            quote = alpaca.get_last_quote(sym)
            bid = quote.bidprice
            last_close = bars[sym][0]['c']
            qty = money.get_num_of_shares(bid)
            cost = qty * bid
            gap = bid - last_close
            table.append([sym, bid , gap, qty, cost, datetime.fromtimestamp(bars[sym][0]['t']), last_close])
        except:
            print("Error getting quote for Symbol: " + sym)
            continue

    headers = ["Symbol", "Current", "Gap", "Shares", "Cost", "time", "Last close"]
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
            pass
            api.submit_order(buying[i][0],buying[i][3],"buy","market","gtc")

if alpaca.is_market_open():
    [print(p.side + " " + p.symbol + " p/l: " + p.unrealized_pl) for p in api.list_positions()]
    print("Waiting for market close")
    time.sleep((alpaca.get_next_close() - now)-420)
    for position in api.list_positions():
        qty = position['qty']
        sym = position['symbol']
        side = "Buying" if position['side']=="long" else "Selling"
        profit_loss = position['unrealized_pl']
        print("{0} {1} shares of {2} p/l: {3}".format(side,qty,sym,profit_loss))

    api.close_all_positions()
    print("Positions closed")

# The End!