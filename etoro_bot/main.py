
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import traceback

from etoro_bot.etoro_bot import TradeActions , EtoroBot
from etoro_bot.assets import BotException, logger, telegram
from etoro_bot import config

from pydantic import BaseModel


class TradeActionParameters(BaseModel):
    trade_action: TradeActions
    symbol: str
    virtual_portfolio : bool = True
    value : int = 50

app = FastAPI()

etoro_bot = EtoroBot(config.selenium_gui ,  )
logger.debug("Bot Loaded")

@app.get("/")
def read_root():
    logger.debug("Hola mundo")
    raise BotException("hola", Exception("ASDF"))

@app.exception_handler(BotException)
def exception_handler(request: Request, exc: BotException):
    return JSONResponse(
        status_code=500,
        content={"ok":"False" , "message": exc.message},
    )

@app.post("/trade")
def trade(trade_action_action : TradeActionParameters):

    global etoro_bot

    reponse = {}
    retries = 3
    while retries > 0:
        try:
            logger.info(f"New Movement {trade_action_action}  ")
            reponse = etoro_bot.launch_bot( **trade_action_action.__dict__) 

            retries = -1

        except Exception:
            retries -= 1
            etoro_bot.end_and_close()
            del etoro_bot
            etoro_bot = EtoroBot(config.selenium_gui ,  )
            error_message = traceback.format_exc()
            
    if retries == 0:
        telegram.send_message(str(trade_action_action.__dict__))
        raise BotException(error_message)
    return reponse
    
