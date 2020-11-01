import pytest

def test_calculate(app):
    app[1].open_calculator_page()
    app[1].get_instruments_list()
