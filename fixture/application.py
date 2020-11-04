# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" %browser)
        self.base_url = base_url

    def open_calculator_page(self):
        wd = self.wd
        wd.get(self.base_url)
        WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.ID, 'header-register')))
        wd.find_element(By.CSS_SELECTOR, '[data-auto="main_menu_Tools___Services"]').click()
        WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="main_menu_Calculator"]'))).click()

    def get_path_current_url(self):
        wd = self.wd
        url = urlparse(wd.current_url)
        return url.path

    def destroy(self):
        self.wd.quit()

    def get_instruments_list(self):
        wd = self.wd
        elements = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="forex"]')))
        instruments = re.split("\n", elements.text)
        return instruments

    def choose_account_type(self,element):
        wd = self.wd
        dropdown = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="account_type"]')))
        dropdown.find_element(By.XPATH, f"//option[. = '{element}']").click()

    def choose_instrument(self,element):
        wd = self.wd
        dropdown = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="forex"]')))
        dropdown.find_element(By.XPATH, f"//option[. = '{element}']").click()

    def choose_lot(self, lot):
        wd = self.wd
        wd.find_element(By.NAME, "lot").click()
        wd.find_element(By.NAME, "lot").clear()
        wd.find_element(By.NAME, "lot").send_keys(lot)

    def choose_leverage(self, leverage):
        wd = self.wd
        dropdown = wd.find_element(By.CSS_SELECTOR, '[data-auto="leverage"]')
        dropdown.find_element(By.XPATH, f"//option[. = '{leverage}']").click()

    def get_calculate(self):
        wd = self.wd
        wd.find_element(By.CSS_SELECTOR, '[data-auto="btn-calc"]').click()

    def get_margin(self):
        wd = self.wd
        element = wd.find_element(By.CSS_SELECTOR, ".table__body .table__cell:nth-child(1)")
        return float(re.split(' ', element.text)[0])

    def get_conversion_factor(self,data_params):
        wd = self.wd
        instrument = data_params["symbol"]
        conversion = {'AUDCHFm': 'AUDUSD',
                      'XAGAUDm': 'XAGUSD',
                      'XAUUSDm': 'XAUUSD',
                      'EURDKKm': 'EURUSD',
                      'AUDSEKm': 'AUDUSD',
                      'USDMXNm': 1,
                      'XPDUSDm': 'XPDUSD',
                      'BTCJPYm': 'BTCUSD',
                      'BCHUSDm': 'BCHUSD'}
        element = wd.find_element_by_xpath(f'//p/ancestor::div//span[contains(text(), {conversion[instrument]})]')

       # element = driver.find_element_by_xpath( "// * [text() = 'Square'] / ancestor::div // * [text() = 'Black']")

        # element = wd.find_element_by_xpath('//div[@class="formula formula--no-border"]//div[@class="formula__item"]/div[1]/p')
        print(element.text)
        return round(float(element.text),5)

    def calculate_with_leverage(self,data_params,conversion_factor,conversion):
        contract_size = {
            'AUDCHFm': 100000,
            'XAGAUDm': 5000,
            'XAUUSDm': 100
        }

        factor = conversion_factor
        instrument = data_params["symbol"]
        if not isinstance(conversion_factor, float):
            factor = conversion_factor[conversion[instrument]]
        margin = round(data_params['lot'] * contract_size[instrument] / int(data_params['leverage']) * factor, 2)
        return margin

    def calculate_with_req_margin(self,data_params,conversion_factor,conversion):
        contract_size_req_margin = {
            'EURDKKm': {'contract_size': 100000,
                        'req_margin': 0.5},
            'AUDSEKm': {'contract_size': 100000,
                        'req_margin': 1},
            'USDMXNm': {'contract_size': 100000,
                        'req_margin': 2},
            'XPDUSDm': {'contract_size': 100,
                        'req_margin': 1},
            'BTCJPYm': {'contract_size': 1,
                        'req_margin': 1},
            'BCHUSDm': {'contract_size': 1,
                        'req_margin': 5}
        }
        factor = conversion_factor
        instrument = data_params["symbol"]
        contract_size = contract_size_req_margin[instrument]['contract_size']
        required_margin = contract_size_req_margin[instrument]['req_margin']
        if conversion[instrument] == 1:
            factor = 1
        elif not isinstance(conversion_factor, float):
            factor = conversion_factor[conversion[instrument]]
        margin = str(round(data_params['lot'] * contract_size * required_margin / 100 * factor, 2))
        return margin

    def calculate_margin(self,data_params,conversion_factor):
        conversion = {'AUDCHFm': 'AUDUSD',
                      'XAGAUDm': 'XAGUSD',
                      'XAUUSDm': 'XAUUSD',
                      'EURDKKm': 'EURUSD',
                      'AUDSEKm': 'AUDUSD',
                      'USDMXNm': 1,
                      'XPDUSDm': 'XPDUSD',
                      'BTCJPYm': 'BTCUSD',
                      'BCHUSDm': 'BCHUSD'}
        margin_with_leverage = ['AUDCHFm','XAGAUDm','XAUUSDm']
        instrument = data_params["symbol"]
        if instrument in margin_with_leverage:
            margin = self.calculate_with_leverage(data_params,conversion_factor,conversion)
            return margin
        else:
            margin = self.calculate_with_req_margin(data_params,conversion_factor, conversion)
            return margin






 # def calculate_margin(self,data_params,conversion_factor):
 #        # conversion = {'AUDCHFm' : 'AUDUSD',
 #        #               'XAGAUDm' : 'XAGUSD',
 #        #               'XAUUSDm' : 'XAUUSD',
 #        #               'EURDKKm' : 'EURUSD',
 #        #               'AUDSEKm' : 'AUDUSD',
 #        #               'USDMXNm' :  1,
 #        #               'XPDUSDm' : 'XPDUSD',
 #        #               'BTCJPYm' : 'BTCUSD',
 #        #               'BCHUSDm' : 'BCHUSD'}
 #        margin_with_leverage = ['AUDCHFm','XAGAUDm','XAUUSDm']
 #        instrument = data_params["symbol"]
 #        # factor = conversion_factor
 #        if instrument in margin_with_leverage:
 #            margin = calculate_with_leverage(self,data_params,conversion_factor)
 #            return margin
 #            # contract_size = {
 #            #     'AUDCHFm' : 100000,
 #            #     'XAGAUDm' : 5000,
 #            #     'XAUUSDm' : 100
 #            # }
 #            # if not isinstance(conversion_factor, float):
 #            #     factor = conversion_factor[conversion[instrument]]
 #            # margin = round(data_params['lot'] * contract_size[instrument] / int(data_params['leverage']) * factor,2)
 #            # return margin
 #        else:
 #            margin = calculate_with_req_margin(self,data_params,conversion_factor)
 #            return margin
 #            # contract_size_req_margin = {
 #            #     'EURDKKm' : {'contract_size' : 100000,
 #            #                  'req_margin' : 0.5},
 #            #     'AUDSEKm' : {'contract_size' : 100000,
 #            #                 'req_margin' : 1},
 #            #     'USDMXNm' : {'contract_size' : 100000,
 #            #                  'req_margin' : 2},
 #            #     'XPDUSDm' : {'contract_size' : 100,
 #            #                  'req_margin' : 1},
 #            #     'BTCJPYm' : {'contract_size' : 1,
 #            #                  'req_margin' : 1},
 #            #     'BCHUSDm' : {'contract_size' : 1,
 #            #                  'req_margin' : 5}
 #            # }
 #            # contract_size = contract_size_req_margin[instrument]['contract_size']
 #            # required_margin = contract_size_req_margin[instrument]['req_margin']
 #            # if conversion[instrument] == 1:
 #            #     factor = 1
 #            # elif not isinstance(conversion_factor, float):
 #            #     factor = conversion_factor[conversion[instrument]]
 #            # margin = str(round(float(data_params['lot']) * contract_size * required_margin / 100 * factor, 2))
 #            #return margin
