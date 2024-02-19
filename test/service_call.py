#!/usr/bin/python3

from enum import Enum

import requests

class TradeActions(str, Enum):
    buy = "buy"
    hold = "hold"
    sell = "sell"

if __name__ == '__main__':

    action = TradeActions.buy
    symbol = "SPX500"
    reponse = requests.post(
        "http://localhost:1888/trade",
        json={
            "trade_action": action,
            "symbol": symbol,
            "virtual_portfolio" : True,
            "value":100
        },
        headers={"accept"  : "application/json",
                "Content-Type":"application/json"}
    )
    print(reponse.json())
