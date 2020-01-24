import json

with open("../data.json") as f:
    data=json.load(f)


for p in data['Bundles']:
    print('you can buy ',p['Products'][0]['Name']+'at our store for',p['Products'][0]['Price'],"$")
