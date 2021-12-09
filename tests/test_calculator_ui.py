import allure
import pytest
from page_objects.MainPage import MainPage
from page_objects.CalculatorPage import CalculatorPage
from data.parameters import data_parameters
from generator.input_params import generate_data


@allure.feature('API TEST: Generate data and put to file data/parameters_mini.json')
def test_generate_data():
    generate_data()


@allure.feature('UI TEST: search calculator')
def test_search_calculator(browser):
    browser.open()
    MainPage(browser) \
        .click_search_icon() \
        .enter_data() \
        .click_search()


@allure.feature('UI TEST: Check language change to PT')
def test_language(browser):
    browser.open('/calculator/')
    CalculatorPage(browser) \
        .change_language_to_pt() \
        .check_path_current_url_pt()


@allure.feature('UI TEST:open page')
def test_open_page(browser):
    browser.open()
    MainPage(browser) \
        .open_calculator_page() \
        .check_path_current_url()


@allure.feature('UI TEST: Check and calculate parameters for Standard account type')
@pytest.mark.parametrize('params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calculate(browser, params):
    browser.open('/calculator/')
    CalculatorPage(browser) \
        .choose_account_type() \
        .choose_instrument(params[0]['instrument']) \
        .choose_lot(str(params[0]["lot"])) \
        .click_calculate()


@allure.feature('UI TEST: Check calculation parameters')
def test_check_parameters(browser):
    browser.open('/calculator/')
    CalculatorPage(browser) \
        .check_margin()
       # .check_pip_value()


@allure.feature('UI TEST: Check currency converter')
def test_check_converter(browser):
    browser.open('/calculator/')
    CalculatorPage(browser) \
        .go_to_converter() \
        .check_path_converter_url()

# @allure.feature('UI TEST: Register user')
# def test_register_user(browser):
#     browser.open('/calculator/')
#     CalculatorPage(browser) \
#         .input_email() \
#         .choose_country()