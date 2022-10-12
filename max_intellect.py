# https://github.com/netology-code/py-homeworks-basic/tree/master/9.http.requests - задание 1
# Программа написана для поиска самого умного супер героя из всего списка героев
# (чтобы это сделать, надо закомментировать строку 6 и раскомментировать строку 7),
# либо выбора самого умного героя из списка.
import requests


def update_dict(in_line, in_heroes_dict):
    if int(in_line['powerstats']['intelligence']) > int(list(in_heroes_dict.values())[0]):
        in_heroes_dict = {in_line['name']: in_line['powerstats']['intelligence']}
    elif int(in_line['powerstats']['intelligence']) == int(list(in_heroes_dict.values())[0]):
        in_heroes_dict.update({in_line['name']: in_line['powerstats']['intelligence']})
    return in_heroes_dict


heroes_list = ['Hulk', 'Captain America', 'Thanos']
# heroes_list = []
req = requests.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json')
if len(heroes_list) > 0:
    search_all = False
else:
    search_all = True
if req.status_code == 200:
    heroes_dict = {'None': 0}
    for line in req.json():
        if search_all is False:
            if line['name'] in heroes_list and len(heroes_list) != 0:
                heroes_dict = update_dict(line, heroes_dict)
                heroes_list.pop(heroes_list.index(line['name']))
        else:
            heroes_dict = update_dict(line, heroes_dict)
    if len(heroes_dict) == 1:
        print(f'Max intellect have {list(heroes_dict.keys())[0]} with {list(heroes_dict.values())[0]}')
    else:
        print('Max intellect have:')
        for line in heroes_dict:
            print(f'{line} with {heroes_dict[line]}')
else:
    print('Error: something goes wrong!')
