
import logging
import datetime

from etoro_bot import config
import requests

logger = logging.getLogger("etoro_bot")
logger.setLevel(logging.DEBUG)

# handler to file
log_filename = "etoro_bot.{:%Y-%m-%d}.log".format(datetime.datetime.now())
handler = logging.FileHandler(log_filename)
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(pathname)s(%(lineno)d):\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


class TelegramSender():
    def __init__(self , telegram_token, telegram_chat_id):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def send_message(self, message):

        send_text = ('https://api.telegram.org/bot' + self.telegram_token + 
                     '/sendMessage?chat_id=' + self.telegram_chat_id + 
                     '&parse_mode=Markdown&text=' + message)

        try:
            response = requests.get(send_text)
            message = response.json()

        except :
            message = {
                    "ok": False ,
                    "message": "Error on telegram API"
                }
        logger.warning( message )
        return message 


telegram = None
if config.enable_telegram:
    telegram = TelegramSender(telegram_token = config.telegram_token, telegram_chat_id= config.telegram_chat_id)


class BotException(Exception):

    def __init__(self, message: str, *args ):
        super().__init__(message , args)
        self.message = message
        logger.error(message)
        if config.enable_telegram:
            telegram.send_message(message)

     