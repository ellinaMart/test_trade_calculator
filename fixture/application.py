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

    def get_audusd(self):
        wd = self.wd
        element = wd.find_element_by_xpath('//div[@class="formula formula--no-border"]//div[@class="formula__item"]/div[1]/p')
        print(element.text)
        return round(float(element.text),5)

    def calculate_margin(self,data_params,AUDUSD):
        margin_with_leverage = ['AUDCADm','AUDCHFm','AUDGBPm','AUDJPYm','AUDNZDm','AUDUSDm','CADCHFm','CADJPYm',
                                'CHFJPYm','EURAUDm','EURCADm','EURCHFm','EURGBPm','EURJPYm','EURNZDm','EURUSDm',
                                'GBPAUDm','GBPCADm','GBPCHFm','GBPJPYm','GBPNZDm','GBPUSDm','HKDJPYm','NZDCADm',
                                'NZDJPYm','NZDUSDm','USDCADm','USDCHFm','USDCNHm','USDHKDm','USDJPYm','USDTHBm',
                                'XAGAUDm','XAGEURm','XAGGBPm','XAGUSDm','XAUAUDm','XAUEURm','XAUGBPm','XAUUSDm']
        if data_params["symbol"] in margin_with_leverage:
            contract_size = 100000
            margin = round(float(data_params['lot']) * contract_size / int(data_params['leverage']) * AUDUSD,2)
            return margin
        else:
            required_margin = 0.5
            contract_size = 100000
            margin = float(data_params['lot']) * contract_size * required_margin / 100
            assert resp.json()["margin"] == str(round(margin* resp.json()['conversion_pairs']['AUDUSD'] * 100, 2))


