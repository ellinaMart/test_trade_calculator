import pytest
import os
import logging
import json

from selenium import webdriver


DRIVERS = os.path.expanduser("~/PycharmProjects/Drivers")
logging.basicConfig(level=logging.INFO, filename="logs/selenium.log")


def pytest_addoption(parser):
    parser.addoption("--browser", "-B", default="chrome")
    parser.addoption("--url", "-U", default="https://www.exness.com")

# @pytest.fixture
# def url(request):
#     return request.config.getoption("--url")

@pytest.fixture
def browser(request):
    """ Фикстура инициализации браузера """
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    logger = logging.getLogger('BrowserLogger')
    test_name = request.node.name

    logger.info("===> Test {} started".format(test_name))

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        driver = webdriver.Chrome(
            options=options,
            executable_path=f"{DRIVERS}/chromedriver"
        )
    elif browser == "firefox":
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(firefox_profile=profile)
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        raise Exception(f"{request.param} is not supported!")

    logger.info("Browser {} started with {}".format(browser, driver.desired_capabilities))

    driver.implicitly_wait(3)
    driver.maximize_window()

    request.addfinalizer(driver.quit)
    def open(path=""):
        return driver.get(url + path)
    driver.open = open
    #driver.open()
    return driver

@pytest.fixture(scope="session", autouse=True)
def get_environment(pytestconfig):
    props = {
        'Shell': os.getenv('SHELL'),
        'Terminal': os.getenv('TERM'),
        'Stand': 'Production'
    }

    tests_root = pytestconfig.rootdir
    with open(f'{tests_root}/allure-results/environment.properties', 'w') as f:
        for k, v in props.items():
            f.write(f'{k}={v}\n')

@pytest.fixture
def get_api_url():
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
        config  = json.load(config_file)
    return config

# @pytest.fixture
# def browser(request):
#     """ Фикстура инициализации браузера """
#
#     browser = request.config.getoption("--browser")
#     url = request.config.getoption("--url")
#
#     # https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
#     common_caps = {"pageLoadStrategy": "none"}
#
#     driver = webdriver.Chrome(
#         executable_path=f"{DRIVERS}/chromedriver",
#         desired_capabilities=common_caps
#     )
#     # else:
#     #
#     #     desired_capabilities = {
#     #         "browser": browser,
#     #         **common_caps
#     #     }
#
#         # driver = webdriver.Remote(
#         #     desired_capabilities=desired_capabilities,
#         #     command_executor=f"http://{executor}:4444/wd/hub",
#         # )
#
#     request.addfinalizer(driver.quit)
#
#     def open(path=""):
#         return driver.get(url + path)
#
#     driver.maximize_window()
#     driver.implicitly_wait(5)
#
#     driver.open = open
#     driver.open()
#
#     return driver

# @pytest.fixture(scope = "module")
# def app(request):
#   global fixture
#   with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
#     config  = json.load(config_file)
#   if fixture is None:
#    fixture = Application(browser= "firefox", base_url = config['base_url'], api_url = config['api_calculator'])
#    #fixture.open_calculator_page()
#
#   request.addfinalizer(fixture.destroy)
#   return fixture


