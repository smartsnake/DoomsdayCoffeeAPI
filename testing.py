from IGUtil import IGUtil
import json

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
ig = IGUtil(data)


ig.getIGOnce()
