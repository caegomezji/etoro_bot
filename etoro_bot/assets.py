
import logging

from etoro_bot import config
import requests


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
        logging.warning(message)
        return message 


telegram = None
if config.enable_telegram:
    telegram = TelegramSender(telegram_token = config.telegram_token, telegram_chat_id= config.telegram_chat_id)


class BotException(Exception):

    def __init__(self, message: str ):
        super().__init__(message)
        logging.error(message)
        if config.enable_telegram:
            telegram.send_message(message)

     