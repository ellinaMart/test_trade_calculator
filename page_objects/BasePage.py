import logging
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from .common.Alert import Alert
from selenium import common
from urllib.parse import urlparse


class BasePage:

    def __init__(self, driver):
        self.driver = driver
       # self.alert = Alert(self.driver)
        self.logger = logging.getLogger(type(self).__name__)

    def __element(self, selector: dict, index: int, link_text: str = None):
        try:
            self.logger.info("Find element {}".format(selector))
            by = None
            if link_text:
                by = By.LINK_TEXT
            if 'xpath' in selector.keys():
                by = By.XPATH
                selector = selector['xpath']
            elif 'css' in selector.keys():
                by = By.CSS_SELECTOR
                selector = selector['css']
            element = self.driver.find_elements(by, selector)[index]
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")
        return element

    def _click_link(self, link_text):
        try:
            element = self.driver.find_element(By.LINK_TEXT, link_text)
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")
        return element

    def _click(self, selector, index=0):
        try:
            self.logger.info("Clicking element: {}".format(selector))
            ActionChains(self.driver).move_to_element(self.__element(selector, index)).click().perform()
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")

    def _wait_click(self, selector, index=0, link_text=None, wait=10):
        try:
            self.logger.info("Clicking element: {}".format(selector))
            element = WebDriverWait(self.driver, wait).until(EC.visibility_of(self.__element(selector, index, link_text)))
            element.click()
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")

    def _input(self, selector, value, index=0):
        try:
            self.logger.info("Input {} in input {}".format(value, selector))
            element = self.__element(selector, index)
            element.clear()
            element.send_keys(value)
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body =self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")

    def _wait_for_visible(self, selector, link_text=None, index=0, wait=20):
        try:
            self.logger.info("Check if element {} is present".format(selector))
            element = WebDriverWait(self.driver, wait).until(EC.visibility_of(self.__element(selector, index, link_text)))
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")
        return element

    def _get_element_text(self, selector, index=0):
        #return self.__element(selector, index).text
        try:
            self.logger.info("Get element {} text".format(selector))
            element = self.__element(selector, index).text
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name = self.driver.session_id,
                body = self.driver.get_screenshot_as_png(),
                attachment_type = allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {selector} not found on page!")
        return element

    def _get_current_url(self):
        url = urlparse(self.driver.current_url)
        return url.path


