
import os 

class Config():

    def __init__(self) -> None:
        self.etoro_user = os.getenv('ETORO_USER')
        self.etoro_pwd = os.getenv('ETORO_PWD')
    
        assert self.etoro_user != None, "Not loaded ETORO_USER values"
        assert self.etoro_pwd != None, "Not loaded ETORO_PWD values"

if __name__ == '__main__':
    print(Config().__dict__)