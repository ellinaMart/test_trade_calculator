from allpairspy import AllPairs
from model.group import Group
import os.path
import json


def generate_data():
    #to generate all pairs put 'instruments' to function parameters
    # parameters = [
    #     instruments,
    #     ["0.01", "0.1", "1", "100", "999999"],
    #     [2, 10, 20, 50, 88, 100, 200, 400, 500, 600, 800, 888, 1000, 1888, 2000],
    #     ["USD"]
    # ]
    parameters = [
        ["EURDKKm","AUDSEKm","USDMXNm","XPDUSDm","BTCJPYm","BCHUSDm","AUDCHFm","XAGAUDm","XAUUSDm"],
        ["0.01", "0.1", "1", "100", "999999"],
        [2, 10, 20, 50, 88, 100, 200, 400, 500, 600, 800, 888, 1000, 1888, 2000],
        ["USD"]
    ]
    global results
    print("PAIRWISE:")
    testdata = []
    for i, pairs in enumerate(AllPairs(parameters)):
        print("{:2d}: {}".format(i, pairs))
        test_data = [
            Group(form_type="mini", instrument="Forex", symbol=pairs[0], lot=pairs[1], leverage=pairs[2],
                  user_currency=pairs[3])]
        testdata.append(test_data)

    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/parameters.json")

    with open(file, "w") as f:
        f.write(json.dumps(testdata,default=lambda x: x.__dict__, indent=2))
