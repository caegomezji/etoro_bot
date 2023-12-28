from typing import Union

from fastapi import FastAPI
from etoro_bot.etoro_bot import TradeActions , launch_bot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/trade")
def trade(trade_action : TradeActions , symbol : str):
    launch_bot(trade_action , symbol=symbol , gui=False)
    return  trade_action
    