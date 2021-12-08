import allure

from .BasePage import BasePage


class MainPage(BasePage):
    TOOLS_SERVICES = {'css': 'li[data-auto="main_menu_Tools___Services"]'}
    CALCULATOR = {'css': 'li[data-auto="main_menu_Calculator"]'}
    SEARCH_ICON = {'css': '[data-auto="icon-search"]'}
    SEARCH_BOX = {'css': '#searchBox'}
    SEARCH = {'css': '[data-auto="search-submit"]'}

    @allure.step("Open calculator page")
    def open_calculator_page(self):
        self._click(self.TOOLS_SERVICES)
        self._click(self.CALCULATOR)
        return self

    @allure.step("Get path of web page")
    def check_path_current_url(self):
        path = self._get_current_url()
        assert '/calculator' in path

    @allure.step("Click search icon")
    def click_search_icon(self):
        self._click(self.SEARCH_ICON)
        return self

    @allure.step("Enter data search")
    def enter_data(self):
        self._input(self.SEARCH_BOX, 'trading calculator')
        return self

    @allure.step("Click search")
    def click_search(self):
        self._click(self.SEARCH)
        return self


    # wd = self.wd
    # wd.get(self.base_url)
    # WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.ID, 'header-register')))
    # wd.find_element(By.CSS_SELECTOR, '[data-auto="main_menu_Tools___Services"]').click()
    # WebDriverWait(wd, 20).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-auto="main_menu_Calculator"]'))).click()


