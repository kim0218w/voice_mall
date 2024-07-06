import json
from datetime import datetime
import os


def record_purchase_history(products_purchased: list):
    file_path = './sub/history/purchase_history.json'
    if os.path.exists(file_path):
        try:
            # 읽고
            with open(file_path, 'r', encoding='utf-8') as file:
                history = json.load(file)

            if len(history) > 50:
                # history 비우기
                history = {}

            # {현재 시간 : 주문된 상품들 정보} 업데이트
            history.update({
                now_time_stamp(): products_purchased
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
                now_time_stamp(): products_purchased
            }

            # 파일에 써주기
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(history, file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(e)


def now_time_stamp() -> str:
    now = datetime.now()
    return f'{now.month}/{now.day}/{now.hour}/{now.minute}'
