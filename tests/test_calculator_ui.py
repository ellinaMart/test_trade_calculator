import pytest
import allure
import time
from data.parameters import data_parameters

# data_parameters = [{'instrument': 'Forex', 'form_type': 'mini', 'leverage': 2,
#                     'lot': 2, 'symbol': 'AUDCHFm', 'user_currency': 'USD'}]

@allure.feature('UI TEST: Check and calculate parameters')
@pytest.mark.parametrize('params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calculate(app, params):
    with allure.step('Открываем страницу калькулятора'):
        app[1].open_calculator_page()
        time.sleep(10)
        assert app[1].get_path_current_url() == '/calculator/'

    with allure.step('Выбираем параметры и нажимаем рассчитать'):
        app[1].choose_account_type("Standard")
        app[1].choose_instrument(params[0]['symbol'])
        app[1].choose_lot(str(params[0]["lot"]))
        app[1].choose_leverage(f"1:{params[0]['leverage']}")
        app[1].get_calculate()

    with allure.step('Рассчитываем margin и сравниваем со значением на странице'):
        margin_ui = app[1].get_margin()
        conversion_factor = app[1].get_conversion_factor(params[0])
        margin_calc = app[1].calculate_margin(params[0],conversion_factor)
        assert margin_ui == margin_calc



