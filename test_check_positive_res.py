import unittest
import string


def check_positive_response(user_input):
    # 정의된 긍정적 응답 목록
    positive_responses = [
        '응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문', '맞아', '네', '예', '맞다', '맞아요'
    ]

    # 입력 받은 문자열에서 구두점 제거
    translator = str.maketrans('', '', string.punctuation)
    cleaned_input = user_input.translate(translator)

    # 공백으로 분리하여 단어 단위로 검사
    words = cleaned_input.split()
    for word in words:
        for response in positive_responses:
            if word.startswith(response):
                return True
    return False


class TestPositiveResponseCheck(unittest.TestCase):
    def test_positive_responses(self):
        # 긍정적인 답변이 포함된 경우
        self.assertTrue(check_positive_response("응, 그걸로 결정했어"))
        self.assertTrue(check_positive_response("네, 주문해주세요"))
        self.assertTrue(check_positive_response("구매해라"))
        self.assertTrue(check_positive_response("어 그래 맞아"))
        self.assertTrue(check_positive_response("맞아"))
        self.assertTrue(check_positive_response("맞다"))
        self.assertTrue(check_positive_response("예"))
        self.assertTrue(check_positive_response("맞아요"))

    def test_negative_responses(self):
        # 긍정적인 답변이 포함되지 않은 경우
        self.assertFalse(check_positive_response("아니, 그건 싫어"))
        self.assertFalse(check_positive_response("그럴 생각 없어"))
        self.assertFalse(check_positive_response("그게 있잖아 "))
        self.assertFalse(check_positive_response(""))


if __name__ == "__main__":
    unittest.main()
