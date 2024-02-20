
import os 

class Config():

    def __init__(self) -> None:

        self.etoro_user = os.getenv('ETORO_USER')
        self.etoro_pwd = os.getenv('ETORO_PWD')

        self.selenium_gui = os.getenv('SELENIUM_GUI', "false").lower() in ('true', '1', 't')
    
        assert self.etoro_user != None, "Not loaded ETORO_USER values"
        assert self.etoro_pwd != None, "Not loaded ETORO_PWD values"

        self.enable_telegram = os.getenv('ENABLE_TELEGRAM', "false").lower() in ('true', '1', 't')

        if self.enable_telegram :

            self.telegram_token = os.getenv( "TELEGRAM_TOKEN" ) 
            self.telegram_chat_id = os.getenv( "TELEGRAM_CHAT_ID" )

            assert self.telegram_token != None, "Not loaded TELEGRAM token"
            assert self.telegram_chat_id != None, "Not loaded TELEGRAM chat id"

if __name__ == '__main__':
    print(Config().__dict__)