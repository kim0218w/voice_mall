import json
from datetime import datetime
import os
# from sub.buy import item


class item:
    name = ''
    price = ''
    arrival_info = ''
    link = ''
    quantity = 0

    def __init__(self, name, price='', arrival_info='', link='', quantity=0):
        self.name = name
        self.price = price
        self.arrival_info = arrival_info
        self.link = link
        self.quantity = quantity


def record_purchase_history(item_purchased: item):
    file_path = './sub/history/purchase_history.json'
    if os.path.exists(file_path):
        try:
            # 읽고
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)

            if now_time_stamp() in history:
                history[now_time_stamp()].append({
                    'name': item_purchased.name, 'link': item_purchased.link, 'quantity': item_purchased.quantity
                })
            else:
                history[now_time_stamp()] = []
                history[now_time_stamp()].append({
                    'name': item_purchased.name, 'link': item_purchased.link, 'quantity': item_purchased.quantity
                })

            # 다시 써주기
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(history, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)

    else:
        try:

            # {현재 시간 : 주문된 상품들 정보} 저장
            history = {
                now_time_stamp(): [
                    {
                        'name': item_purchased.name,
                        'link': item_purchased.link,
                        'quantity': item_purchased.quantity
                    }
                ]
            }

            # 파일에 써주기
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(history, file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(e)


def now_time_stamp() -> str:
    now = datetime.now()
    return f'{now.month}/{now.day}'


test_item1 = item(name='[새로운상회] 새 제품1', link='https://www.example.com', quantity=1)
test_item2 = item(name='[새로운상회] 새 제품2', link='https://www.example.com', quantity=2)
test_item3 = item(name='[새로운상회] 새 제품3', link='https://www.example.com', quantity=3)
test_item4 = item(name='[새로운상회] 새 제품4', link='https://www.example.com', quantity=4)
test_item5 = item(name='[새로운상회] 새 제품5', link='https://www.example.com', quantity=5)

record_purchase_history(test_item1)
record_purchase_history(test_item2)
record_purchase_history(test_item3)
record_purchase_history(test_item4)
record_purchase_history(test_item5)
