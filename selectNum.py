def selectNum(self,input):
    order_dict = {
        '첫째': 1,'첫번째': 1,'일': 1,'일번': 1,'하나' : 1,
        '둘째': 2,'두번째': 2,'이': 2,'이번': 2,'둘' : 2,
        '셋째': 3,'셋번째': 3,'삼': 3,'삼번': 3,'셋' : 3,
        '넷째': 4,'네번째': 4,'사': 4,'사번': 4,'넷' : 4
    }
    # 예시 사용법
    if input in order_dict:
        number = order_dict[input]
    else:
        print('잘못된 선택입니다')
    return number