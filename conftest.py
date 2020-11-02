import pytest
import json
import os
from fixture.application import Application

fixture = None


@pytest.fixture(scope = "module")
def app(request):
  global fixture
  with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config  = json.load(config_file)
  if fixture is None:
   fixture = Application(browser= "firefox", base_url = config['url_calculator'])
   #fixture.open_calculator_page()

  request.addfinalizer(fixture.destroy)
  return config, fixture


# @pytest.fixture(scope = "module")
# def get_config():
#     with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
#         config = json.load(config_file)
#     return config







