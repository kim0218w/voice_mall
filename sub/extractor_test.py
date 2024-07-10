import re


# # 예시 사용
# input_text = '예시는 네번째'
# print(selectNum(input_text))


class ProductQuantityExtractor:
    def __init__(self):
        # 1부터 100까지 한글 수량을 숫자로 변환하기 위한 딕셔너리
        self.korean_to_number = {
            "한": "1", "하나": "1", "두": "2", "둘": "2", "세": "3", "셋": "3", "네": "4",  "넷": "4", "다섯": "5", "여섯": "6", "일곱": "7", "여덟": "8", "아홉": "9", "열": "10",
            "열한": "11", "열하나": "11", "열두": "12", "열둘": "12", "열세": "13", "열셋": "13", "열네": "14", "열넷": "14", "열다섯": "15", "열여섯": "16", "열일곱": "17", "열여덟": "18", "열아홉": "19",
            "스물": "20", "스물하나": "21", "스물한": "21", "스물두": "22", "스물둘": "22", "스물세": "23", "스물셋": "23", "스물넷": "24",  "스물네": "24", "스물다섯": "25", "스물여섯": "26", "스물일곱": "27", "스물여덟": "28", "스물아홉": "29",
            "서른": "30", "서른한": "31", "서른하나": "31", "서른두": "32", "서른둘": "32", "서른세": "33", "서른셋": "33",  "서른네": "34", "서른넷": "34", "서른다섯": "35", "서른여섯": "36", "서른일곱": "37", "서른여덟": "38", "서른아홉": "39",
            "마흔": "40", "마흔한": "41", "마흔하나": "41", "마흔두": "42", "마흔둘": "42", "마흔세": "43", "마흔셋": "43", "마흔네": "44", "마흔넷": "44",  "마흔다섯": "45", "마흔여섯": "46", "마흔일곱": "47", "마흔여덟": "48", "마흔아홉": "49",
            "쉰": "50", "쉰한": "51", "쉰하나": "51", "쉰두": "52", "쉰둘": "52",  "쉰세": "53", "쉰셋": "53", "쉰네": "54", "쉰넷": "54",  "쉰다섯": "55", "쉰여섯": "56", "쉰일곱": "57", "쉰여덟": "58", "쉰아홉": "59",
            "예순": "60", "예순한": "61", "예순하나": "61", "예순두": "62", "예순둘": "62", "예순세": "63", "예순셋": "63",  "예순네": "64", "예순넷": "64",  "예순다섯": "65", "예순여섯": "66", "예순일곱": "67", "예순여덟": "68", "예순아홉": "69",
            "일흔": "70", "일흔한": "71", "일흔하나": "71", "일흔두": "72", "일흔둘": "72", "일흔세": "73", "일흔셋": "73", "일흔네": "74", "일흔넷": "74",  "일흔다섯": "75", "일흔여섯": "76", "일흔일곱": "77", "일흔여덟": "78", "일흔아홉": "79",
            "여든": "80", "여든한": "81", "여든하나": "81", "여든두": "82", "여든둘": "82",  "여든세": "83", "여든셋": "83", "여든넷": "84", "여든네": "84", "여든다섯": "85", "여든여섯": "86", "여든일곱": "87", "여든여덟": "88", "여든아홉": "89",
            "아흔": "90", "아흔하나": "91", "아흔한": "91", "아흔두": "92", "아흔둘": "92", "아흔세": "93", "아흔셋": "93", "아흔네": "94", "아흔넷": "94",  "아흔다섯": "95", "아흔여섯": "96", "아흔일곱": "97", "아흔여덟": "98", "아흔아홉": "99",
        }
    # 한글을 숫자로 표시

    def convert_korean_numbers(self, text):
        strange_input = {'한계': 1, '하나': 1, '크게': 2, '투개': 2, '세계': 3}

        keys = list(strange_input.keys())

        if text in keys:
            return strange_input[text]

        for korean, number in self.korean_to_number.items():
            text = re.sub(r'\b' + korean + r'\b', number, text)
            if '개' in text:
                for i in range(len(text)):
                    if text[i] == '개':
                        text = str(text[:i]).strip()
                        try:
                            if text in self.korean_to_number:
                                return int(self.korean_to_number[text])
                            else:
                                return int(text)
                        except Exception as e:
                            print(e)
                            return None

    def convert_unit(self, unit):
        if unit in ['그람', '그램']:
            return 'g'
        elif unit == '리터':
            return 'L'
        return unit if unit else ''

    def extract(self, text):

        # 정규 표현식을 사용하여 상품명과 수량 추출
        pattern = re.compile(r'([가-힣]+\d*[그람|그램|리터]*)\s?(\d+)?\s?[개권통대g]*')

        # 필터링 단어 리스트 (필요에 따라 추가)
        filter_words = ['사줘', '해', '장바구니로', '주문', '안녕', '와', '추가로', '주문해줘', '그리고', '하지만', '주문해줘', '주문 해달라고', '주문해']

        # 결과 저장을 위한 리스트
        result = []
        matches = pattern.findall(text)
       # 추출된 상품명과 수량을 리스트에 저장
        for match in matches:
            item, quantity = match
            if item not in filter_words:
                quantity = quantity if quantity else ''
                result.append(item)

        return result

    def selectNum(self, input):
        self.order_dict = {
            '첫째': 1, '첫번째': 1,
            '둘째': 2, '두번째': 2,
            '셋째': 3, '세번째': 3,
            '넷째': 4, '네번째': 4,
        }

        # 입력 문자열을 단어 단위로 분리하여 처리
        words = input.split()
        for word in words:
            # 각 단어가 패턴(숫자)에 매칭되는지 확인
            if word in self.order_dict:
                number = self.order_dict[word]
                return number

        return None

    # {월}/{일}(요일)을 {월}월{일}일{요일}로 변환하는 함수
    def format_dates(self, input_string):
        special_not = ['내일', '오늘', '모레']

        for notation in special_not:
            if notation in input_string:
                return input_string

        if input_string is None:
            return None  # None 입력 처리
        # 문자열 형식 변환 함수
        formatted_string = re.sub(r'(\d+)/(\d+)\((\w+)\)', r'\1월\2일\3', input_string)
        return formatted_string if formatted_string != input_string else None  # 패턴 미일치 시 None 반환
