import sub.make_voice as mv
import sub.extractor_test as ex
import sub.buy as buy
import os
from STT import listen_to_client as ltc
import sub.chat as chat
import sub.history.purchase_history as ph

id = os.getenv('COUPANG_ID')
pw = os.getenv('COUPANG_PW')

lc = ltc.listen_to_client()
ai_name = '안녕'
sound_path = './sound/'


class controller:

    selen = None

    def __init__(self):
        self.stage = 'call_ai'
        self.order = ''  # 사람 말을 여기다 저장
        self.order_search_word = []  # 주문 검색 목록 저장 (보통 카테고리가 저장됨 eg: {item:딸기, quantity:10})
        self.order_item = []  # item class 인스턴스가 들어감
        self.add_order_items = []  # 추가 주문 목록 저장

    def recognize_voice_interface(self):
        go_to_stage = {
            'call_ai': self.ai호출,
            'order_listen': self.주문듣기,
            'order_confirm': self.주문확인,
            'order_search': self.주문검색,
            'order_add': self.주문추가,
            'end': self.끝
        }
        # stage에 맞는 함수 반환
        return go_to_stage[self.stage]

    def ai호출(self):
        # ai 부르는 거 듣기
        call_ai = lc.listen(duration=3)  # 2초
        if ai_name in call_ai:
            chat.cm.write_chat(chat.chat('client', ai_name))
            # order stage로 이동
            self.stage = 'order_listen'

    def 주문듣기(self):

        # 사용자에게 주문받는 다는 신호를 주고
        chat.cm.write_chat(chat.chat('ai', '주문받는중'))
        mv.playsound(sound_path + 'water_drop.mp3')

        # 주문듣기 10초
        self.order = lc.listen(10)
        print(self.order)
        chat.cm.write_chat(chat.chat('client', self.order))

        chat.cm.write_chat(chat.chat('ai', '주문확인중'))
        mv.playsound(sound_path + 'order_checking.mp3')  # 주문확인중

        self.stage = 'order_confirm'  # 주문확인으로 이동

    def 주문확인(self):

        # 말에서 주문 추출
        self.order_search_word = ex.ProductQuantityExtractor().extract(self.order)
        # print(self.order_items)
        if len(self.order_search_word) == 0:
            chat.cm.write_chat(chat.chat('ai', '주문하시려면 다시 저를 불러주세요'))
            mv.playsound(sound_path + 'call_me_again.mp3')  # 주문하시려면 다시 저를 불러주세요
            self.stage = 'call_ai'  # 다시 ai 호출을 기다리도록 함
            return

        # 주문한 상품이 정확한지 확인하기
        voice = '주문하신 상품이\n'
        for product in self.order_search_word:
            voice += f'{product["item"]}, {product["quantity"]}개\n'
        voice += '맞으십니까?'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)  # 확인하는 음성출력
        mv.playsound(sound_path + 'water_drop.mp3')

        # 주문 확인 받기
        res = lc.listen(4)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        # 긍정응답이 존재하는지 확인
        for answer_yes in ['응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문', '맞아', '네']:
            if '안해' not in res and '취소' not in res and answer_yes in res:
                chat.cm.write_chat(chat.chat('ai', "주문중"))
                mv.playsound(sound_path + 'ordering.mp3')  # 주문중 안내
                self.stage = 'order_search'  # 주문검색
                return

        # 주문실패
        chat.cm.write_chat(chat.chat('ai', '다시 주문해주세요'))
        mv.playsound(sound_path + 'get_back_order.mp3')  # 다시 주문해주세요
        self.stage = "order_listen"  # 다시 주문으로 이동

    # 주문을 검색 + 사용자에게 어떤 상품을 고르겠냐고 물어봄
    def 주문검색(self):

        try:
            self.selen = buy.buyBySelenium()
            self.selen.go_to_mall()  # 홈페이지 이동
            self.selen.login()  # 홈페이지 로그인
            for search_word in self.order_search_word:
                print(search_word)
                voice = f'{search_word["item"]}를 검색합니다.'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)  # 음성만들고 출력

                self.selen.search_item(search_word['item'])  # 검색
                items = self.selen.get_related_items()  # 검색된 창에서 상품 상위 4개 추출
                voice = '상위 4개의 상품 중에\n'
                i = 1
                for item in items:
                    voice += f'{i}번. {item.name} {item.price}원, {item.arrival_info}\n'
                    i += 1

                voice += '들이 있어요. 어떤 걸 고르시겠어요? 1 2 3 4 로 말해주세요'
                mv.make_voice(voice)  # 음성만들고 출력
                res = lc.listen(3)  # 주문에 대한 확인 음성 받기
                chat.cm.write_chat(chat.chat('client', res))
                # selected = items[int(res)-1]
                selected = items[0]  # 테스트용
                selected.quantity = int(search_word['quantity'])  # 상품 개수 넣어주고
                self.selen.go_to_add_cart(selected)     # 장바구니에 담으러 감
                ph.record_purchase_history(selected)  # 구매이력 담기
                self.stage = "order_add"
        except Exception as e:
            print(e)
            mv.playsound(sound_path+'something_wrong.mp3')
            self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함

    def 주문추가(self):
        # 추가하실 것이 더 있습니까?
        chat.cm.write_chat(chat.chat('ai', "추가하실 것이 더 있으신가요?"))
        mv.playsound(sound_path + 'is_there_something_to_add.mp3')
        mv.playsound(sound_path + 'water_drop.mp3')

        # 주문 확인 받기
        res = lc.listen(2)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        for answer_yes in ['응', '그렇게 해', '어', '그래', '맞아', '네']:
            if '안해' not in res and '취소' not in res and answer_yes in res:
                # 추가주문해주세요
                chat.cm.write_chat(chat.chat('ai', "추가 주문해주세요"))
                mv.playsound(sound_path + 'add_items_in_cart.mp3')
                self.stage = 'order_listen'  # 주문듣기로 이동
                return

        # 장바구니로 이동합니다.
        self.stage = 'end'

    def 끝(self):

        try:
            # 요청하신 상품을 장바구니에 모두 담았습니다.
            chat.cm.write_chat(chat.chat('ai', "요청하신 상품을 장바구니에 모두 담았습니다"))
            mv.playsound(sound_path + 'request_item_all_clear.mp3')

        except Exception as e:
            print(e)
            mv.playsound(sound_path+'something_wrong.mp3')

        finally:
            self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함
