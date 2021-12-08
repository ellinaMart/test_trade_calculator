# import requests
# import os
# import json
# import pytest
# import allure
# from page_objects.CalculatorPage import CalculatorPage
# from data.parameters import data_parameters
# from generator.input_params import generate_data
#
# @allure.feature('API TEST: Generate data')
# def test_generate_data(browser):
#     with allure.step("Генерируем тестовые данные в файл data/parameters_mini.json"):
#         generate_data()
#         # browser.open('/calculator/')
#         # CalculatorPage(browser) \
#         #     .generate_data()
#
#
# @allure.feature('API TEST: Get and check data parameters')
# @pytest.mark.parametrize('data_params', data_parameters, ids=[repr(x) for x in data_parameters])
# def test_calc(get_api_url, data_params):
#     print(data_params)
#     # payload = {
#     #     "operationName": "Calculate",
#     #     "variables": {
#     #         "input": data_params[0]
#     #     }
#     # }
#     payload = {"operationName":"Calculate",
#                "variables":
#                    {"input":
#                         {"account_type":"mt5_mini_real_vc",
#                          "currency":"USD",
#                          "instrument":"1INCHUSDm",
#                          "leverage":200,
#                          "lot":0.01
#                          }
#                     },
#                "query":"mutation Calculate($input: CalculationInput!) {\n  calculate(input: $input) {\n    currency\n    margin\n    pip_value\n    swap_long\n    swap_short\n    __typename\n  }\n}\n"}
#     resp = requests.get(get_api_url['api_calculator'], payload=payload)
#     import pdb; pdb.set_trace()
#
#     print(resp.text)
#     assert resp.json()["margin"]
#     assert resp.status_code == 200
# #
# #     with allure.step("Проверяем параметр margin по формулам"):
# #         conversion_factor = resp.json()['conversion_pairs']
# #         margin = app.calculate_margin(data_params[0], conversion_factor)
# #         assert round(float(resp.json()["margin"]),1) == round(float(margin),1)
