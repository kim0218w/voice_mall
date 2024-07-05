import speech_recognition as sr
import extractor as ex
import make_voice as mv
import buy

class OrderProcessor:
    def __init__(self):
        self.r = sr.Recognizer()  # 음성을 듣는 객체 생성
        self.expect_yes_res = ['응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문']
        self.pqe = ex.ProductQuantityExtractor()  # 상품 추출 객체 생성

    def listen_and_recognize(self, source, timeout, phrase_time_limit):
        print('듣고있어요')
        audio = self.r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        text = self.r.recognize_google(audio, language='ko')
        return text

    def process_order(self, order_text):
        result = self.pqe.extract(order_text)
        return result

    def generate_confirmation_voice(self, products):
        voice = '주문하신 상품이\n'
        for product in products:
            voice += f'{product["item"]}, {product["quantity"]}개\n'
        voice += '맞으십니까?'
        return voice

    def is_confirmation_positive(self, response):
        for r in self.expect_yes_res:
            if '안해' not in response and '취소' not in response and r in response:
                return True
        return False

    def run(self):
        with sr.Microphone() as source:
            try:
                text = self.listen_and_recognize(source, timeout=1, phrase_time_limit=5)
                print(text)
                if '광태' in text:
                    # 비프음 출력
                    mv.playsound('water_drop.mp3')
                    print('주문받는중')
                    order = self.listen_and_recognize(source, timeout=5, phrase_time_limit=10)
                    print(order)

                    # 음성으로 받은 텍스트에서 상품 추출하기
                    result = self.process_order(order)
                    print(result)

                    # 주문하신 상품이 정확한지 확인하기
                    print("void_recg 주문확인")
                    confirmation_voice = self.generate_confirmation_voice(result)
                    mv.make_voice(confirmation_voice)  # 확인하는 음성출력

                    response = self.listen_and_recognize(source, timeout=5, phrase_time_limit=5)
                    if self.is_confirmation_positive(response):
                        print("주문이 확인되었습니다.")
                        return result, True
                    else:
                        print("주문이 취소되었습니다.")
                        return None, False

            except Exception as e:
                print(e)
                return None, False

# # 사용 예시
# order_processor = OrderProcessor()
# order_processor.run()
