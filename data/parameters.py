import os.path
import json

with open(os.path.join(os.path.dirname(__file__), 'parameters_mini.json')) as parameters_file:
    data_parameters = json.load(parameters_file)