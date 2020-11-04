import requests
import os
import json
import pytest
import allure
from generator.input_params import generate_data
from data.parameters import data_parameters

@allure.feature('API TEST: Generate data')
def test_generate_data(app):
    with allure.step("Получаем список инструментов для формы standart и генерируем тестовые данные в файл data/parameters_mini.json"):
        #app[1].open_calculator_page()
        #instruments = app[1].get_instruments_list()
        generate_data()

@allure.feature('API TEST: Get and check data parameters')
@pytest.mark.parametrize('data_params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calc(app, data_params):
    with allure.step("Отправляем запрос на расчет параметров со сгенерированными тестовыми данными"):
        print(data_params)
        resp = requests.get(app[0]["api_calculator"], params=data_params[0])
        print(resp.text)
        assert resp.json()["margin"]
        assert resp.status_code == 200

    with allure.step("Проверяем параметр margin по формулам"):
        conversion_factor = resp.json()['conversion_pairs']
        margin = app[1].calculate_margin(data_params[0], conversion_factor)
        assert round(float(resp.json()["margin"]),1) == round(float(margin),1)
