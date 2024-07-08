import sub.make_voice as mv
import sub.extractor as ex
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

    def __init__(self):
        self.stage = 'call_ai'
        self.order = ''
        self.order_items = []
        self.response_about_order_confirm = False

    def recognize_voice_interface(self):
        go_to_stage = {
            'call_ai': self.ai호출,          # ai 호출
            'order': self.주문받기,          # 주문
            'order_confirm': self.주문확인,  # 주문확인
            'go_to_mall': self.장바구니담기,
            'order_add': self.주문추가       # 주문추가
        }
        # stage에 맞는 함수 반환
        return go_to_stage[self.stage]

    def ai호출(self):
        # ai 부르는 거 듣기
        call_ai = lc.listen(duration=3)  # 2초
        if ai_name in call_ai:
            chat.cm.write_chat(chat.chat('client', ai_name))
            # order stage로 이동
            self.stage = 'order'

    def 주문받기(self):

        # 사용자에게 주문받는 다는 신호를 주고
        chat.cm.write_chat(chat.chat('ai', '주문받는중'))
        mv.playsound(sound_path + 'water_drop.mp3')
        print('주문받는중')

        # 주문듣기 10초
        self.order = lc.listen(10)
        print(self.order)
        chat.cm.write_chat(chat.chat('client', self.order))

        chat.cm.write_chat(chat.chat('ai', '주문확인중'))
        mv.playsound(sound_path + 'order_checking.mp3')  # 주문확인중

        self.stage = 'order_confirm'  # 주문확인으로 이동

    def 주문확인(self):

        self.order_items = ex.ProductQuantityExtractor().extract(self.order)
        print(self.order_items)
        if len(self.order_items) == 0:
            chat.cm.write_chat(chat.chat('ai', '주문하시려면 다시 저를 불러주세요'))
            mv.playsound(sound_path + 'call_me_again.mp3')  # 주문확인중
            self.stage = 'call_ai'  # 다시 ai 호출을 기다리도록 함
            return

        # 주문한 상품이 정확한지 확인하기
        voice = '주문하신 상품이\n'
        for product in self.order_items:
            voice += f'{product["item"]}, {product["quantity"]}개\n'
        voice += '맞으십니까?'

        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)  # 확인하는 음성출력

        res = lc.listen(2)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))
        for answer_yes in ['응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문']:
            if '안해' not in res and '취소' not in res and answer_yes in res:
                chat.cm.write_chat(chat.chat('ai', "주문중"))
                mv.playsound(sound_path + 'ordering.mp3')  # 주문중 안내
                self.stage = 'go_to_mall'  # 장바구니에 담으러 이동
                return

        # 긍정응답이 없을 경우
        chat.cm.write_chat(chat.chat('ai', '다시 주문해주세요'))
        mv.playsound(sound_path + 'get_back_order.mp3')  # 다시 주문해주세요
        self.stage = "order"  # 다시 주문으로 이동

    def 장바구니담기(self):

        id = os.getenv('COUPANG_ID')
        pw = os.getenv('COUPANG_PW')
        try:

            go_to_mall = buy.buyBySelenium()
            go_to_mall.getUserInfo(id, pw)
            go_to_mall.login()
            go_to_mall.searchItem(self.order_items)
            go_to_mall.cart()

            # 요청하신 상품을 장바구니에 모두 담았습니다.
            chat.cm.write_chat(chat.chat('ai', "요청하신 상품을 장바구니에 모두 담았습니다"))
            mv.playsound(sound_path + 'request_item_all_clear.mp3')
            ph.record_purchase_history(self.order_items)

        except Exception as e:
            print(e)
            mv.playsound(sound_path+'something_wrong.mp3')

        finally:
            self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함

    def 주문추가():
        pass
