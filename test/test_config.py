#!/bin/
import unittest

from etoro_bot import config
from etoro_bot.assets import TelegramSender


config.enable_telegram = False

class TestStringMethods(unittest.TestCase):

    def test_config(self):
        assert config.etoro_user != None, "Not loaded config values"
        assert config.etoro_pwd != None, "Not loaded config values"
        
    @unittest.skipIf( not config.enable_telegram , "Integration Test: Telegram not enabled")
    def test_send_telegram(self):

        message = "testing telegram integration"

        telegram = TelegramSender(telegram_token=config.telegram_token , telegram_chat_id=config.telegram_chat_id)
        telegram_response = telegram.send_message(message)
        assert "ok" in telegram_response , "unrecognizable format"
        assert telegram_response["ok"], "getting errors on instagram api"
        


if __name__ == '__main__':
    unittest.main()