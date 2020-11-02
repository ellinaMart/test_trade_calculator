import pytest
#import allure

#@allure.feature('Calculate parameters')
def test_calculate(app):
    #with allure.step('Открываем страницу калькулятора'):
    app[1].open_calculator_page()
    assert app[1].get_path_current_url() == '/calculator/'

    #with allure.step('Выбираем параметры и нажимаем рассчитать'):
    app[1].choose_account_type("Raw Spread")
    app[1].choose_instrument("AUDCHF")
    app[1].choose_lot(2)
    app[1].choose_leverage("1:2")
    app[1].get_calculate()
    assert app[1].get_margin()


