import requests
import os
import json
import pytest
#import allure
from generator.input_params import generate_data
from data.parameters import data_parameters

#@allure.feature('Generate data')
def test_generate_data(app):
    # with allure.step("Получаем список инструментов для формы standart и генерируем тестовые данные в файл data/parameters.json"):
    app[1].open_calculator_page()
    instruments = app[1].get_instruments_list()
    generate_data(instruments)

#@allure.feature('Get and check data')
@pytest.mark.parametrize('data_params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calc(app, data_params):
    #with allure.step("Отправляем запрос на расчет параметров со сгенерированными тестовыми данными"):
    print(data_params)
    resp = requests.get(app[0]["api_calculator"], params=data_params[0])
    print(resp.text)
    assert resp.json()["margin"]
    assert resp.status_code == 200

    #with allure.step("Проверяем параметр margin по формулам"):
    margin_without_leverage = ['EURDKKm','EURNOKm','USDDKKm','USDNOKm','USDSEKm','USDSGDm','USDZARm']
    if data_params[0]["symbol"] in margin_without_leverage:
        required_margin = 0.5
        contract_size = 100000
        margin = float(data_params[0]['lot']) * contract_size * required_margin/100
        assert resp.json()["margin"] == str(round(margin* resp.json()['conversion_pairs']['AUDUSD'] * 100, 2))
    else:
        contract_size = 1000
        margin = float(data_params[0]['lot']) * contract_size / int(data_params[0]['leverage'])
        assert resp.json()["margin"] == str(round(margin * resp.json()['conversion_pairs']['AUDUSD'] * 100, 2))


