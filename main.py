#https://www.albion-online-data.com/api/v2/stats/prices/T4_BAG,T5_BAG?locations=Caerleon,Bridgewatch&qualities=2
import time
import re
import requests


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
            profit_percentage = list[i][1]['buy_price_max'] / list[i][0]['sell_price_min']
            if profit_percentage > 0.5:
                list[i].append(round(profit_percentage, 2) * 100)
                returned_list.append(list[i])
        except ZeroDivisionError:
            pass
    return returned_list


start = time.time()
line_request = ''
template = re.compile(r"\w\d_(\w)*_(\w)*_(\w)*")
corect_items = ''
with open('items_Id.txt') as f:
    for line in f:
        corect_item =  re.search(r"\w[45678]_(\w)*_PLATE_(\w)*", line) #створив шаблон для пошуку id
        if corect_item:
            corect_items += corect_item.group() + '\n'
#print(corect_items)
items = [i for i in corect_items.split('\n')]
#print(len(items))
chunk_items = []
items_information = []
for item in range(len(items)):
    if len(chunk_items) != 100:
        chunk_items.append(items[item]) #створення чанку по 20 предметів
    else:
        req = requests.get(f'https://www.albion-online-data.com/api/v1/stats/prices/{",".join(chunk_items)}?locations=BlackMarket,Lymhurst').json()
        items_information += req
        chunk_items = []
formated_items = []
for i in range(len(items_information)):
    if items_information[i]['sell_price_max'] or items_information[i]['buy_price_min']:
        formated_items.append(items_information[i])
#print(formated_items)
sorted_item = sort(formated_items)
print(check_profit(sorted_item))
#print(f'https://www.albion-online-data.com/api/v2/stats/prices/{",".join(chunk_items)}?locations=BlackMarket,Lymhurst')

