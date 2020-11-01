import pytest
import json
import os

@pytest.fixture(scope = "module")
def get_config():
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
        config = json.load(config_file)
    return config