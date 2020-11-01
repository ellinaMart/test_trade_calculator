import requests
import os
import json
import pytest

from data.parameters import data_parameters


@pytest.mark.parametrize('data_params', data_parameters, ids=[repr(x) for x in data_parameters])
def test_calc(get_config, data_params):
    # data_params1= {
    #         "form_type" : "cent",
    #         "instrument" : "Forex",
    #         "symbol" : "AUDCADc",
    #         "lot" : 0.01,
    #         "leverage" : 2,
    #         "user_currency" : "USC"
    #         }
    print(data_params)
    resp = requests.get(get_config["url_calculator"], params=data_params[0])
    print(resp.text)

    assert resp.json()["margin"]
    assert resp.status_code == 200

