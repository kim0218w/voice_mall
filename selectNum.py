import re

def selectNum(input):
    order_dict = {
        '첫째': 1, '첫번째': 1,
        '둘째': 2, '두번째': 2,
        '셋째': 3, '셋번째': 3,
        '넷째': 4, '네번째': 4,
    }
    
    # 입력 문자열을 단어 단위로 분리하여 처리
    words = input.split()
    for word in words:
        # 각 단어가 패턴(숫자)에 매칭되는지 확인
        if word in order_dict:
            number = order_dict[word]
            return number
    
    print('잘못된 선택입니다')
    return None

# 예시 사용
input_text = '예시는 네번째'
print(selectNum(input_text))
