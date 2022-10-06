# https://github.com/netology-code/py-homeworks-basic/tree/master/9.http.requests - задание 1

import requests

heroes_list = ['Hulk', 'Captain America', 'Thanos']
# heroes_list = None
req = requests.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json')
tmp = {'None': 0}

for line in req.json():
    if heroes_list is not None:
        if line['name'] in heroes_list:
            if int(line['powerstats']['intelligence']) > int(list(tmp.values())[0]):
                tmp = {line['name']: line['powerstats']['intelligence']}
    else:
        if int(line['powerstats']['intelligence']) > int(list(tmp.values())[0]):
            tmp = {line['name']: line['powerstats']['intelligence']}
        elif int(line['powerstats']['intelligence']) == int(list(tmp.values())[0]):
            tmp.update({line['name']: line['powerstats']['intelligence']})

if len(tmp) == 1:
    print(f'Max intellect have {list(tmp.keys())[0]} with {list(tmp.values())[0]}')
else:
    print('Max intellect have:')
    for line in tmp:
        print(f'{line} with {tmp[line]}')
