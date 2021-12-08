from allpairspy import AllPairs
from model.group import Group
import os.path
import json


def generate_data():
    # to generate all pairs put 'instruments' to function parameters
    parameters = [
        ["mini"],
        ["EURDKKm","AUDSEKm","USDMXNm","XPDUSDm","BTCJPYm","BCHUSDm","AUDCHFm","XAGAUDm","XAUUSDm"],
        [0.01, 0.1, 1, 100, 999999],
        [2, 10, 100, 2000],
        ["USD"]
    ]
    # global results
    print("PAIRWISE:")
    testdata = []
    for i, pairs in enumerate(AllPairs(parameters)):
        print("{:2d}: {}".format(i, pairs))
        test_data = [
            Group(account_type=pairs[0], instrument=pairs[1], lot=pairs[2], leverage=pairs[3],
                  currency=pairs[4])]
        testdata.append(test_data)

    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/parameters_mini1.json")

    with open(file, "w") as f:
        f.write(json.dumps(testdata,default=lambda x: x.__dict__, indent=2))
