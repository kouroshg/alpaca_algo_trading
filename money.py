
import math

class manage:
    def __init__(self, available_fund, max_trade_count):
        self.available_fund = available_fund
        self.max_trade_count = max_trade_count

    def get_num_of_shares(self, price_per_share):
        fund = math.floor(self.available_fund/self.max_trade_count)
        return math.floor(fund/price_per_share)