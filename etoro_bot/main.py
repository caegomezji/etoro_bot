
from fastapi import FastAPI
import traceback

from etoro_bot.etoro_bot import TradeActions , launch_bot
from etoro_bot.assets import BotException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/trade")
def trade(trade_action : TradeActions , symbol : str):
    try:
        launch_bot(trade_action , symbol=symbol , gui=False)
    except Exception:
        raise BotException("Critical error on app: " + traceback )
    return  trade_action
    