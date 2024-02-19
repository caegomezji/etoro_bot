#!/usr/bin/python3

import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from selenium.webdriver import ActionChains

from etoro_bot import config
from etoro_bot.assets import logger

from enum import Enum

class TradeActions(str, Enum):
    buy = "buy"
    hold = "hold"
    sell = "sell"


#uc.TARGET_VERSION = 85

class EtoroBot():

    def __init__(self,gui = False):
        self.driver = self.load_driver(gui)
        user = config.etoro_user
        pwd = config.etoro_pwd
        self.in_virtual = False
        #driver = load_driver(gui = gui)
        if self.driver == None:
            raise Exception("Not loaded")
        self.login(self.driver, user, pwd)

        time.sleep(1)

    def load_driver( self, gui = False):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

        desired_capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities['user_agent'] = user_agent

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--window-size=1920,1080')

        options.add_argument(f"--user-agent={user_agent}")
        print( f"gui: {gui}")
        driver = uc.Chrome( headless=not gui,
            desired_capabilities=desired_capabilities, options=options, version_main=120)
        return driver

    def login(self, driver, user, pwd):

        driver.get('https://www.etoro.com/login')
        #driver.get('http://localhost:9999')

        time.sleep(6)
        #assert "Facebook" in driver.title
        print("Logging in...")
        elem = driver.find_element(By.ID, "username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "password")
        elem.send_keys(pwd)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        try:
            wait_ele = EC.presence_of_element_located(
                (By.CLASS_NAME, 'i-menu-user-username'))
            elem = driver.find_element(By.CLASS_NAME, "i-menu-user-username")
        except TimeoutException:
            print("Loading took too much time!")
        except:
            pass
        if (elem != None) and (elem.text == user):
            print("logged in")
        else:
            print("wtf?")
        time.sleep(2)


    def find_elements_by_automation_id(self,driver_element, automation_id):
        return driver_element.find_elements(By.CSS_SELECTOR, '[automation-id="{}"]'.format(automation_id))


    def find_elements_by_data_etoro_automation_id(self,driver_element, automation_id):
        return driver_element.find_elements(By.CSS_SELECTOR, '[data-etoro-automation-id="{}"]'.format(automation_id))

    def _close_position(self, order_cell):

        buttons = self.find_elements_by_automation_id(
            order_cell, "group-actions-dropdown-3dots")
        assert len(buttons) == 1, " it brings more than 1 button"
        button = buttons[0]
        button.click()

        time.sleep(1)

        dropdowns = self.find_elements_by_automation_id(
            self.driver, "group-actions-instrument-container")
        assert len(dropdowns) == 1, " it brings more than 1 dropdown"
        dropdown = dropdowns[0]

        spans = dropdown.find_elements(By.TAG_NAME, "span")
        assert len(spans) != 0, " it brings more than 1 span"

        for span in spans:
            print(span.text)
            if span.text == "Close All":
                span.click()

                time.sleep(1)

                close_buttons = self.find_elements_by_data_etoro_automation_id(
                    self.driver, "close-all-positions-closs-all-button")
                print(close_buttons)
                assert len(
                    close_buttons) == 1, " it brings more than 1 button"
                close_button = close_buttons[0]

                current_value_spans = self.find_elements_by_data_etoro_automation_id(self.driver, "close-all-positions-last-price-value")
                assert len(current_value_spans) == 1, f" it brong {current_value_spans} current value spans"
                current_value_span = current_value_spans[0]
                current_value= float(current_value_span.text.strip().replace("$" , ""))

                close_button.click()
                time.sleep(1)
                return current_value


    def _close_position_get_active_orders_cells(self ):

        self.driver.get("https://www.etoro.com/portfolio/positions")
        time.sleep(6)
        elements = self.find_elements_by_automation_id(
            self.driver,  "watchlist-grid-instruments-list")
        assert elements != None, "elements is None"
        assert len(elements) > 0, "elements is empty"
        # driver.find_elements
        print("elements ", elements)
        order = dict()
        index = 0
        for e in elements:

            symbol_div = self.find_elements_by_automation_id(
                e,  "portfolio-overview-table-body-cell-market-name")
            assert symbol_div != None, "symbol_div is None"
            assert len(symbol_div) > 0, "symbol_div is empty"

            if len(symbol_div) > 0:
                symbol = symbol_div[0].text
                print("symbol" , symbol)
                order[symbol] = e
                index += 1
        return order
        
    def close_positions(self, symbols):

        orders = self._close_position_get_active_orders_cells()

        for symbol in symbols:
            try: 
                assert symbol in orders.keys(), "{} not found".format(symbol)
                current_value = self._close_position(orders[symbol])
                orders[symbol] = current_value
            except Exception as e:
                orders[symbol] = -1
                print("error", e)
                pass
        return orders



    def open_sell_position(self,driver, symbol, price):
        driver.get("https://www.etoro.com/markets/{}/chart".format(symbol.lower()))
        time.sleep(6)

        trade_button_parents_wraps = self.find_elements_by_automation_id(
            driver, "market-page-header-wrapp")
        assert len(
            trade_button_parents_wraps) == 1, " it brings more than 1 button wrap"
        trade_button_parents_wrap = trade_button_parents_wraps[0]

        trade_button_parents_wrap = self.find_elements_by_automation_id(
            trade_button_parents_wrap, "market-page-header-trade-button-regular")
        assert len(trade_button_parents_wrap) == 1, " it brings more than 1 button"
        trade_button_parent = trade_button_parents_wrap[0]

        trade_buttons = self.find_elements_by_automation_id(
            trade_button_parent, "trade-button")
        print(trade_buttons)
        assert len(trade_buttons) == 1, " it brings more than 1 button"
        trade_button = trade_buttons[0]
        trade_button.click()

        # open the buy/sell menu
        time.sleep(3)

        sell_chip = self.find_elements_by_automation_id(driver, "open-position-sell-chip")
        assert len(sell_chip) == 1, "Error: it brings " + str(len(sell_chip)) + "sell chips"
        sell_chip = sell_chip[0]
        sell_chip.click()
        time.sleep(1)

        value_inputs = self.find_elements_by_automation_id(driver, "open-position-amount-input-amount")
        assert len(value_inputs) == 1, " it brings more than 1 value inputs"
        value_input = value_inputs[0]

        action = ActionChains(driver)
        action.double_click(value_input).perform()

        value_input.send_keys(price)
        value_input.send_keys(Keys.RETURN)

        time.sleep(1)
        entry_order_buttons = self.find_elements_by_automation_id(
            driver, "open-position-by-value-submit-button")
        assert len(entry_order_buttons) == 1, " it brings more than 1 entry button"
        entry_order_button = entry_order_buttons[0]

        current_value_spans = self.find_elements_by_automation_id(driver, "open-position-by-value-current-rate-with-short-symbol")
        assert len(current_value_spans) == 1, f" it brong {current_value_spans} current value spans"
        current_value_span = current_value_spans[0]
        current_value= float(current_value_span.text.strip().replace("$" , ""))

        entry_order_button.click()

        time.sleep(1)
        return current_value
    
    def open_buy_position(self,driver, symbol, price):
        tries = 3
        while (tries > 0):

            driver.get("https://www.etoro.com/markets/{}/chart".format(symbol.lower()))
            time.sleep(6 + abs(3 - tries))

            trade_button_parents_wraps = self.find_elements_by_automation_id(
                driver, "market-page-header-wrapp")
            if len( trade_button_parents_wraps) == 1:
                break
            
            tries -= 1
            logger.warning(f"Retry try {tries}")
            

            
            
            
        assert len(
            trade_button_parents_wraps) == 1, " it brings more than 1 button wrap"
        trade_button_parents_wrap = trade_button_parents_wraps[0]

        trade_button_parents_wrap = self.find_elements_by_automation_id(
            trade_button_parents_wrap, "market-page-header-trade-button-regular")
        assert len(trade_button_parents_wrap) == 1, " it brings more than 1 button"
        trade_button_parent = trade_button_parents_wrap[0]

        trade_buttons = self.find_elements_by_automation_id(
            trade_button_parent, "trade-button")
        print(trade_buttons)
        assert len(trade_buttons) == 1, " it brings more than 1 button"
        trade_button = trade_buttons[0]
        trade_button.click()

        # open the buy/sell menu
        time.sleep(3)

        value_inputs = self.find_elements_by_automation_id(driver, "open-position-amount-input-amount")
        assert len(value_inputs) == 1, " it brings more than 1 value inputs"
        value_input = value_inputs[0]

        action = ActionChains(driver)
        action.double_click(value_input).perform()

        value_input.send_keys(price)
        value_input.send_keys(Keys.RETURN)

        time.sleep(1)
        entry_order_buttons = self.find_elements_by_automation_id(
            driver, "open-position-by-value-submit-button")
        assert len(entry_order_buttons) == 1, " it brings more than 1 entry button"
        entry_order_button = entry_order_buttons[0]

        current_value_spans = self.find_elements_by_automation_id(driver, "open-position-by-value-current-rate-with-short-symbol")
        assert len(current_value_spans) == 1, f" it brong {current_value_spans} current value spans"
        current_value_span = current_value_spans[0]
        current_value= float(current_value_span.text.strip().replace("$" , ""))
        
        entry_order_button.click()

        time.sleep(1)
        return current_value


    def go_to_virtual_portfolio(self,driver):

        virtual_buttons = self.find_elements_by_automation_id(
            driver, "sidenav-switch-to-virtual")
        assert len(virtual_buttons) == 1, " it brings more than 1 virtual button"
        virtual_button = virtual_buttons[0]
        virtual_button.click()
        time.sleep(1)

        toogle_button = driver.find_element(By.CLASS_NAME, "toggle-account-button")
        assert toogle_button != None, " toogle_button is None"
        toogle_button.click()

        time.sleep(1)

    def go_to_real_portfolio(self,driver):

        virtual_buttons = self.find_elements_by_automation_id(
            driver, "sidenav-switch-to-real")
        assert len(virtual_buttons) == 1, " it brings more than 1 virtual button"
        virtual_button = virtual_buttons[0]
        virtual_button.click()
        time.sleep(1)

        toogle_button = driver.find_element(By.CLASS_NAME, "toggle-account-button")
        assert toogle_button != None, " toogle_button is None"
        toogle_button.click()

        time.sleep(1)


    def launch_bot(self, trade_action: TradeActions, symbol , virtual_portfolio = True , value = 50):
        action = trade_action


        if (virtual_portfolio and not self.in_virtual):
            self.go_to_virtual_portfolio(self.driver)
            time.sleep(3)
            self.in_virtual = True

        if ( not virtual_portfolio and self.in_virtual):
            self.go_to_real_portfolio(self.driver)
            time.sleep(3)
            self.in_virtual = False

        current_value = -1
        if action == TradeActions.hold:
            current_value = self.close_positions([symbol])[symbol]

        if action == TradeActions.buy:
            current_value = self.open_buy_position(self.driver, symbol, value)

        if action == TradeActions.sell:
            current_value = self.open_sell_position(self.driver, symbol, value)

        time.sleep(1)

        csv_file_name = "saves.csv"

        with open(csv_file_name, 'a') as f:

            f.write("{},{},{},{}\n".format(
                symbol, action, value, current_value, virtual_portfolio , datetime.datetime.now()))
        
    
        return {"reponse": "ok" , "current_value" : current_value}
    
    def end_and_close(self):
        self.driver.close()
        self.driver.quit()
        logger.debug("Exit chromium")


if __name__ == '__main__':
    action = TradeActions.buy
    etoro_bot = EtoroBot( True)
    result = etoro_bot.launch_bot(action , symbol="SPX500" , virtual_portfolio= True)
    print(result)
