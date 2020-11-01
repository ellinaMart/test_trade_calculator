import pytest

def test_calculate(app):
    app[1].open_calculator_page()
    app[1].choose_account_type("Raw Spread")
    app[1].choose_instrument("AUDCHFm")


