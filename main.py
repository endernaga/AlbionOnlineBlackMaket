#https://www.albion-online-data.com/api/v2/stats/prices/T4_BAG,T5_BAG?locations=Caerleon,Bridgewatch&qualities=2
import time
import re
import requests
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def sort(list):
    returned_list = []
    num = 0
    while num < len(list) - 1:
        if list[num]['item_id'] == list[num + 1]['item_id']:
            returned_list.append([list[num], list[num + 1]])
            num += 2
        else:
            num += 1
    return returned_list


def check_profit(list):
    returned_list = []
    for i in range(len(list)):
        try:
            profit_percentage = (list[i][0]['sell_price_min'] - list[i][1]['sell_price_min']) / list[i][1]['sell_price_min']
            if profit_percentage > 0.5:
                list[i].append(round(profit_percentage, 2) * 100)
                returned_list.append(list[i])
        except ZeroDivisionError:
            pass
    return returned_list

def show_data(list):
    for i in list:
        print(f'Товар {i[0]["item_id"]} з відсотком окупа {i[2]} з ціною покупки {i[1]["sell_price_min"]} і продажі {i[0]["sell_price_min"]}')

start = time.time()
line_request = ''
template = re.compile(r"\w\d_(\w)*_(\w)*_(\w)*")
corect_items = ''
with open(resource_path('items_Id.txt')) as f:
    for line in f:
        corect_item =  re.search(r"\w[45678]_(\w)*_CLOTH_(\w)*", line) #створив шаблон для пошуку id
        if corect_item:
            corect_items += corect_item.group() + '\n'
#print(corect_items)
items = [i for i in corect_items.split('\n')]
#print(len(items))
chunk_items = []
items_information = []
for item in range(len(items)):
    if len(chunk_items) != 100:
        chunk_items.append(items[item]) #створення чанку по 100 предметів
    else:
        req = requests.get(f'https://www.albion-online-data.com/api/v1/stats/prices/{",".join(chunk_items)}?locations=BlackMarket,FortSterlingPortal').json()
        items_information += req
        chunk_items = []
else:
    req = requests.get(
        f'https://www.albion-online-data.com/api/v1/stats/prices/{",".join(chunk_items)}?locations=BlackMarket,FortSterlingPortal').json()
    items_information += req
formated_items = []
for i in range(len(items_information)):
    if items_information[i]['sell_price_max'] or items_information[i]['buy_price_min']:
        formated_items.append(items_information[i])
#print(formated_items)
sorted_item = sort(formated_items)
print(sorted_item)
checked_profit = check_profit(sorted_item)
show_data(checked_profit)
input()
#print(f'https://www.albion-online-data.com/api/v2/stats/prices/{",".join(chunk_items)}?locations=BlackMarket,Lymhurst')

