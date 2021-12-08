import re
import allure

from .BasePage import BasePage

class CalculatorPage(BasePage):
    ACCOUNT_TYPE = {'css': '[name="account_type"]'}
    STANDARD = {'css': 'option[value="mt5_mini_real_vc"]'}
    INSTRUMENT_LIST = {'css': 'select[name="instrument"]'}
    LOT = {'css': 'input[class="inp__field"]'}
    CALCULATE = {'css': 'button[data-auto="btn-calc"]'}
    MARGIN = {'css': '.table__body .table__cell:nth-child(1)'}
    PIP = {'css': '.table__body .table__cell:nth-child(2)'}
    LANGUAGE_DROPDOWN = {'css': '[id="language-icon"]'}
    LANGUAGE = {'css': '[data="pt"]'}

    @allure.step("Get instrument list")
    def get_instruments_list(self):
        self._click(self.INSTRUMENT_LIST)
        import pdb; pdb.set_trace()
       # elements = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="forex"]')))
        #instruments = re.split("\n", elements.text)
        #return instruments

    @allure.step("Choose account type")
    def choose_account_type(self):
        self._wait_for_visible(self.ACCOUNT_TYPE)
        self._wait_click(self.ACCOUNT_TYPE)
        self._wait_click(self.STANDARD)

        # element_text = self._get_element_text(self.ACCOUNT_TYPE)
        # import pdb; pdb.set_trace()
        # if element_text == "Standard":
        #     pass
        # else:
        #     self._click(self.ACCOUNT_TYPE)
        #     self._click(self.STANDARD)
        return self
       # dropdown = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="account_type"]')))
       # dropdown.find_element(By.XPATH, f"//option[. = '{element}']").click()

    @allure.step("Choose instrument")
    def choose_instrument(self, element):
        instrument = {'css': f'option[value="{element}"]'}
        self._wait_click(self.INSTRUMENT_LIST)
        self._wait_click(instrument)
        return self
        #dropdown = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="forex"]')))
        #dropdown.find_element(By.XPATH, f"//option[. = '{element}']").click()

    @allure.step("Change language")
    def change_language_to_pt(self):
        self._click(self.LANGUAGE_DROPDOWN)
        self._wait_click(self.LANGUAGE)
        return self

    @allure.step("Check url for language")
    def check_path_current_url_pt(self):
        path = self._get_current_url()
        assert '/pt/calculator' in path

    @allure.step("Choose count of lots")
    def choose_lot(self, lot):
        self._click(self.LOT, index=1)
        self._input(self.LOT, lot, index=1)
        return self

    # def choose_leverage(self, leverage):
    #     wd = self.wd
    #     dropdown = wd.find_element(By.CSS_SELECTOR, '[data-auto="leverage"]')
    #     dropdown.find_element(By.XPATH, f"//option[. = '{leverage}']").click()

    @allure.step("Calculate")
    def click_calculate(self):
        self._click(self.CALCULATE)
        return self

    @allure.step("Check margin")
    def check_margin(self):
        element_text = self._get_element_text(self.MARGIN)
       # import pdb; pdb.set_trace()
        print(element_text)
        #margin_value = float(re.split(' ', element_text)[0])
        assert element_text is not None

    @allure.step("Check pip value")
    def check_pip_value(self):
        element_text = self._get_element_text(self.PIP)
        print(element_text)
        #pip_value = float(re.split(' ', element_text)[0])
        assert element_text is not None

    def get_conversion_factor(self,data_params):
        instrument = data_params["symbol"]
        conversion = {'AUDCHFm': 'AUDUSD',
                      'XAGAUDm': 'XAGUSD',
                      'XAUUSDm': 'XAUUSD',
                      'EURDKKm': 'EURUSD',
                      'AUDSEKm': 'AUDUSD',
                      'USDMXNm': 1,
                      'XPDUSDm': 'XPDUSD',
                      'BTCJPYm': 'BTCUSD',
                      'BCHUSDm': 'BCHUSD'}
        if conversion[instrument] == 1:
            return 1
        else:
            element = WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.XPATH, f'//span[contains(text(), "{conversion[instrument]}")]/ancestor::div/p')))
            #element = wd.find_element_by_xpath(f'//span[contains(text(), "{conversion[instrument]}")]/ancestor::div/p')
            print(element.text)
            return round(float(element.text), 5)

    def calculate_with_leverage(self,data_params,conversion_factor,conversion):
        contract_size = {
            'AUDCHFm': 100000,
            'XAGAUDm': 5000,
            'XAUUSDm': 100
        }

        factor = conversion_factor
        instrument = data_params["symbol"]
        if not isinstance(conversion_factor, float):
            factor = conversion_factor[conversion[instrument]]
        margin = round(data_params['lot'] * contract_size[instrument] / int(data_params['leverage']) * factor, 2)
        return margin

    def calculate_with_req_margin(self,data_params,conversion_factor,conversion):
        contract_size_req_margin = {
            'EURDKKm': {'contract_size': 100000,
                        'req_margin': 0.5},
            'AUDSEKm': {'contract_size': 100000,
                        'req_margin': 1},
            'USDMXNm': {'contract_size': 100000,
                        'req_margin': 2},
            'XPDUSDm': {'contract_size': 100,
                        'req_margin': 1},
            'BTCJPYm': {'contract_size': 1,
                        'req_margin': 1},
            'BCHUSDm': {'contract_size': 1,
                        'req_margin': 5}
        }
        factor = conversion_factor
        instrument = data_params["symbol"]
        contract_size = contract_size_req_margin[instrument]['contract_size']
        required_margin = contract_size_req_margin[instrument]['req_margin']
        if conversion[instrument] == 1:
            factor = 1
        elif not isinstance(conversion_factor, float):
            factor = conversion_factor[conversion[instrument]]
        margin = round(data_params['lot'] * contract_size * required_margin / 100 * factor, 2)
        return margin

    def calculate_margin(self,data_params,conversion_factor):
        conversion = {'AUDCHFm': 'AUDUSD',
                      'XAGAUDm': 'XAGUSD',
                      'XAUUSDm': 'XAUUSD',
                      'EURDKKm': 'EURUSD',
                      'AUDSEKm': 'AUDUSD',
                      'USDMXNm': 1,
                      'XPDUSDm': 'XPDUSD',
                      'BTCJPYm': 'BTCUSD',
                      'BCHUSDm': 'BCHUSD'}
        margin_with_leverage = ['AUDCHFm','XAGAUDm','XAUUSDm']
        instrument = data_params["symbol"]
        if instrument in margin_with_leverage:
            margin = self.calculate_with_leverage(data_params,conversion_factor,conversion)
            return margin
        else:
            margin = self.calculate_with_req_margin(data_params,conversion_factor, conversion)
            return margin

