import requests
import pytest
import allure

from data.parameters import data_parameters
from generator.input_params import generate_data


@allure.feature('API TEST: Generate data')
def test_generate_data(browser):
    generate_data()


@allure.feature('API TEST: Get and check data parameters')
@pytest.mark.parametrize('data_params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calc(get_api_url, data_params):
    print(data_params)
    data_params[0]["account_type"] = "mt5_mini_real_vc"
    payload = {"operationName": "Calculate",
               "variables":
                   {"input": data_params[0]
                    },
               "query": "mutation Calculate($input: CalculationInput!) {\n  calculate(input: $input) {\n    currency\n "
                        "   margin\n    pip_value\n    swap_long\n    swap_short\n    __typename\n  }\n}\n"}
    resp = requests.post(get_api_url['api_calculator'], json=payload)
    print(resp.text)
    assert resp.json()['data']['calculate']['margin']
    assert resp.status_code == 200
