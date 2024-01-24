
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import traceback

from etoro_bot.etoro_bot import TradeActions , EtoroBot
from etoro_bot.assets import BotException, logger


from pydantic import BaseModel


class TradeActionParameters(BaseModel):
    trade_action: TradeActions
    symbol: str
    virtual_portfolio : bool = True

app = FastAPI()

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
    reponse = {}
    try:
        print(trade_action_action.trade_action , trade_action_action.symbol )
        logger.debug(trade_action_action.trade_action )
        logger.debug(trade_action_action.symbol )
        etoro_bot = EtoroBot()
        reponse = etoro_bot.launch_bot(
            trade_action_action.trade_action ,
            symbol=trade_action_action.symbol, 
            virtual_portfolio=trade_action_action.virtual_portfolio)

    except Exception:
        raise BotException(traceback.format_exc())
    finally:
        etoro_bot.end_and_close()
        del etoro_bot
    return reponse
    
