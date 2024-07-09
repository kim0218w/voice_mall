import re

def selectNum(input):
    order_dict = {
        '첫째': 1, '첫번째': 1, '일': 1, '일번': 1, '하나': 1,
        '둘째': 2, '두번째': 2, '이': 2, '이번': 2, '둘': 2,
        '셋째': 3, '셋번째': 3, '삼': 3, '삼번': 3, '셋': 3,
        '넷째': 4, '네번째': 4, '사': 4, '사번': 4, '넷': 4
    }
    
    # 정규표현식 패턴 설정
    pattern = r'\b(첫째|첫번째|일|일번|하나|둘째|두번째|이|이번|둘|셋째|셋번째|삼|삼번|셋|넷째|네번째|사|사번|넷)\b'
    
    # 입력 문자열에서 패턴에 맞는 단어 찾기
    match = re.search(pattern, input)
    if match:
        word = match.group(0)
        number = order_dict[word]
        return number
    else:
        print('잘못된 선택입니다')
        return None
