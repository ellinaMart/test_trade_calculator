# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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

    def destroy(self):
        self.wd.quit()

    def go_to_calculator(self):
        wd = self.wd
        wd.get(self.base_url)

    def get_instruments_list(self):
        wd = self.wd
        elements = wd.find_elements(By.NAME, "forex")
        instruments = re.split("\n", elements[0].text)
        return instruments

    # def click_calculate(self):
    #     wd = self.wd
    #     wd.find_element(By.XPATH, )

    # def write_letter(self, letter):
    #     wd = self.wd
    #     wd.find_element(By.XPATH, '//div[text()="Написать"]').click()
    #     WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.NAME, 'to'))).send_keys(letter.email_to)
    #     wd.find_element(By.NAME, 'subjectbox').send_keys(letter.email_subject)
    #     wd.find_element(By.XPATH, '//div[text()="Отправить"]').click()
    #     WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Письмо отправлено."]')))
    #     time.sleep(10)
    #
    # def go_to_sent_letters(self):
    #     wd = self.wd
    #     wd.find_element(By.XPATH, '//a[text()="Отправленные"]').click()
    #
    # def get_email_list(self):
    #     wd = self.wd
    #     letters = []
    #     wd.implicitly_wait(50)
    #     elements = wd.find_elements_by_xpath('//div[@class="xT"]/div[@class="y6"]/span[@class="bog"]/span')
    #     for element in elements:
    #         text_element = element.text
    #         letters.append(text_element)
    #     return letters




