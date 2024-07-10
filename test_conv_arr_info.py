import unittest
import re


def format_dates(input_string):
    if input_string is None:
        return None  # None 입력 처리
    # 문자열 형식 변환 함수
    formatted_string = re.sub(r'(\d+)/(\d+)\((\w+)\)', r'\1월\2일\3', input_string)
    return formatted_string if formatted_string != input_string else None  # 패턴 미일치 시 None 반환


class TestFormatDates(unittest.TestCase):
    def test_valid_date_formats(self):
        # 정상적인 날짜 형식 입력
        self.assertEqual(format_dates("7/10(화)"), "7월10일화")
        self.assertEqual(format_dates("7/11(수)"), "7월11일수")
        self.assertEqual(format_dates("7/12(목)"), "7월12일목")
        self.assertEqual(format_dates("7/13(금)"), "7월13일금")
        self.assertEqual(format_dates("7/14(토)"), "7월14일토")

    def test_none_input(self):
        # None 입력 처리
        self.assertIsNone(format_dates(None))

    def test_invalid_pattern_input(self):
        # 패턴에 맞지 않는 입력
        self.assertIsNone(format_dates("This is not a date pattern"))
        self.assertIsNone(format_dates("12345"))
        self.assertIsNone(format_dates("July 10th, Tuesday"))


if __name__ == '__main__':
    unittest.main()
