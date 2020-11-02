import pytest
#import allure
import time

data_parameters = [{'instrument': 'Forex', 'form_type': 'mini', 'leverage': 2,
                    'lot': 2, 'symbol': 'AUDCHFm', 'user_currency': 'USD'}]

#@allure.feature('UI TEST: Check and calculate parameters')
@pytest.mark.parametrize('params', data_parameters)
def test_calculate(app, params):
    #with allure.step('Открываем страницу калькулятора'):
    app[1].open_calculator_page()
    assert app[1].get_path_current_url() == '/calculator/'
    time.sleep(10)

    #with allure.step('Выбираем параметры и нажимаем рассчитать'):
    app[1].choose_account_type("Standard")
    app[1].choose_instrument(params["symbol"])
    app[1].choose_lot(params["lot"])
    app[1].choose_leverage("1:2")
    app[1].get_calculate()

    # with allure.step('Рассчитываем margin и сравниваем со значением на странице'):
    margin_ui = app[1].get_margin()
    AUDUSD = app[1].get_audusd()
    margin_calc = app[1].calculate_margin(params,AUDUSD)
    assert margin_ui == margin_calc


