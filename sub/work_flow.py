import sub.make_voice as mv
import sub.extractor_test as ex
import sub.buy as buy
import os
from STT import listen_to_client as ltc
import sub.chat as chat
import sub.history.purchase_history as ph
from datetime import datetime
import sub.error.error_handle as error
err = error.error()

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
        self.order_search_word = []  # 주문 검색 목록 저장 (보통 카테고리가 저장됨 eg: [딸기,토마토])
        self.order_items = []  # item class 인스턴스가 들어감

    def recognize_voice_interface(self):
        go_to_stage = {
            'call_ai': self.ai호출,
            'order_listen': self.주문듣기,
            'order_confirm': self.주문확인,
            'order_search': self.주문검색,
            'order_add': self.주문추가,
            'end': self.끝,
            'order_recent_items': self.가장최근구매상품주문,
            'order_items_in_day': self.특정일구매상품주문,
            'order_items_in_bookmark': self.즐겨찾기구매
        }
        # stage에 맞는 함수 반환
        return go_to_stage[self.stage]

    def ai호출(self):
        # ai 부르는 거 듣기
        call_ai = lc.listen(duration=3)  # 3초
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
        chat.cm.write_chat(chat.chat('client', self.order))

        if '최근' in self.order:
            # 가장 최근에 구매했던 상품들 바로 주문
            self.stage = 'order_recent_items'
            return

        elif '즐겨' in self.order:
            # 즐겨찾기 주문
            self.stage = 'order_items_in_bookmark'
            return
        elif '월' in self.order and '일' in self.order:
            # 땡월 땡일에 구매했던 상품들 바로 주문
            self.stage = 'order_items_in_day'
            return

        chat.cm.write_chat(chat.chat('ai', '주문확인중'))
        mv.playsound(sound_path + 'order_checking.mp3')  # 주문확인중

        self.stage = 'order_confirm'  # 주문확인으로 이동

    def 주문확인(self):

        # 말에서 주문 추출
        self.order_search_word = ex.ProductQuantityExtractor().extract(self.order)

        if len(self.order_search_word) == 0:
            chat.cm.write_chat(chat.chat('ai', '주문하시려면 다시 저를 불러주세요'))
            mv.playsound(sound_path + 'call_me_again.mp3')  # 주문하시려면 다시 저를 불러주세요
            self.stage = 'call_ai'  # 다시 ai 호출을 기다리도록 함
            return

        # 주문한 상품이 정확한지 확인하기
        voice = '주문하신 상품이\n'
        for product in self.order_search_word:
            voice += f'{product}\n'
        voice += '맞으십니까?'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)  # 확인하는 음성출력
        mv.playsound(sound_path + 'water_drop.mp3')
        chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))
        # 주문 확인 받기
        res = lc.listen(4)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        # 긍정응답이 존재하는지 확인
        for answer_yes in ['응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문', '맞아', '네']:
            if '안해' not in res and '취소' not in res and answer_yes in res:
                chat.cm.write_chat(chat.chat('ai', "쿠팡으로 이동합니다."))
                mv.playsound(sound_path + 'go_to_coupang.mp3')  # 주문중 안내
                self.stage = 'order_search'  # 주문검색
                return

        # 주문실패
        chat.cm.write_chat(chat.chat('ai', '다시 주문해주세요'))
        mv.playsound(sound_path + 'get_back_order.mp3')  # 다시 주문해주세요
        self.stage = "call_ai"  # 다시 주문으로 이동

    # 주문을 검색 + 사용자에게 어떤 상품을 고르겠냐고 물어봄
    def 주문검색(self):

        try:
            self.selen = buy.buyBySelenium()
            self.selen.go_to_mall()  # 홈페이지 이동
            self.selen.login()  # 홈페이지 로그인
            for search_word in self.order_search_word:
                # print(search_word)
                voice = f'{search_word}를 검색합니다.'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)  # 음성만들고 출력

                #### 검색 ####
                self.selen.search_item(search_word)  # 검색
                items = self.selen.get_related_items()  # 검색된 창에서 상품 상위 4개 추출

                #### 상품 선택 ####
                voice = '상위 4개의 상품 중에\n'
                i = 1
                for item in items:
                    voice += f'{i}번. {item.name} {item.price}원, {item.arrival_info}\n'
                    i += 1

                voice += '들이 있어요. 어떤 걸 고르시겠어요? 1번째 2번째 3번째 4번째 로 말해주세요'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)  # 음성만들고 출력
                mv.playsound(sound_path + 'water_drop.mp3')
                chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))
                res = lc.listen(3)  # 주문에 대한 확인 음성 받기
                # print(res)
                chat.cm.write_chat(chat.chat('client', res))
                ITEM_NUM = ex.ProductQuantityExtractor().selectNum(res)

                #### 수량 설정 ####
                # 상품을 주문합니다. 몇 개를 주문하시겠어요?
                voice = f'{ITEM_NUM}번째 상품을 주문합니다. 몇 개를 주문하시겠어요?'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)  # 음성만들고 출력
                mv.playsound(sound_path + 'water_drop.mp3')
                chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

                # 수량받기
                res = lc.listen(3)  # 주문에 대한 확인 음성 받기
                chat.cm.write_chat(chat.chat('client', res))
                ITEM_QUAN = ex.ProductQuantityExtractor().convert_korean_numbers(res)

                #### 최종 확인 ####
                # 몇 번째 상품 + 수량 맞으십니까?
                voice = f'{ITEM_NUM}번째 상품 {ITEM_QUAN}개 맞으십니까?'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)  # 음성만들고 출력
                mv.playsound(sound_path + 'water_drop.mp3')
                chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

                res = lc.listen(3)  # 주문에 대한 확인 음성 받기
                chat.cm.write_chat(chat.chat('client', res))

                is_success = False

                #### 주문 ####
                # 긍정응답이 존재하는지 확인
                for answer_yes in ['응', '그렇게 해', '어', '그래', '구매해', '주문해', '구매', '주문', '맞아', '네']:
                    if '안해' not in res and '취소' not in res and answer_yes in res:

                        #### 구매 세팅 ####
                        selected = items[ITEM_NUM-1]
                        selected.quantity = ITEM_QUAN
                        # selected = items[0]  # for test 1번째 상품을 고름
                        # selected.quantity = 3  # for test 수량 3개로 받음

                        #### 주문 ####
                        chat.cm.write_chat(chat.chat('ai', "주문중"))
                        mv.playsound(sound_path + 'ordering.mp3')  # 주문중 안내
                        self.selen.go_to_add_cart(selected)     # 장바구니에 담으러 감
                        ph.record_purchase_history(selected)  # 구매이력 담기
                        self.order_items.append(selected)  # 구매된거 담기
                        is_success = True
                        break
                if is_success == False:
                    # 주문실패
                    chat.cm.write_chat(chat.chat('ai', '주문이 담기지 않았아요'))
                    mv.playsound(sound_path + 'do_not_your_request.mp3')

            self.stage = 'order_add'  # 주문 추가 여부를 물어보러 이동

        except Exception as e:

            if len(self.order_items) != 0:
                mv.make_voice('주문이 되지 않은게 있어요. 나중에 추가해주세요')
                self.stage = 'order_add'  # 주문 추가 여부를 물어보러 이동
            else:
                err.write(e, '주문검색 에러')
                mv.playsound(sound_path+'something_wrong.mp3')
                self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함

    def 주문추가(self):
        # 추가하실 것이 더 있습니까?
        chat.cm.write_chat(chat.chat('ai', "추가하실 것이 더 있으신가요? 예, 아니오로 대답해주세요"))
        mv.playsound(sound_path + 'is_there_something_to_add.mp3')
        mv.playsound(sound_path + 'water_drop.mp3')
        chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

        # 주문 확인 받기
        res = lc.listen(4)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        if '예' in res:
            # 추가주문해주세요
            chat.cm.write_chat(chat.chat('ai', "주문을 해주세요."))
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

            # 즐겨찾기 등록
            chat.cm.write_chat(chat.chat('ai', '즐겨찾기로 설정할까요? 즐겨찾기는 한 개만 저장할 수 있어요. 예 아니오로 대답해주세요'))
            mv.playsound(sound_path + 'do_you_want_reg_items_in_bookmark.mp3')
            mv.playsound(sound_path + 'water_drop.mp3')
            chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

            res = lc.listen(4)
            chat.cm.write_chat(chat.chat('client', res))

            # 즐겨찾기 등록
            if '예' in res:
                # 즐겨찾기 추가
                chat.cm.write_chat(chat.chat('ai', "방금 주문하신 상품들을 즐겨찾기로 설정할게요"))
                mv.playsound(sound_path + 'set_bookmark.mp3')

                # 즐겨찾기 추가하는 함수
                ph.record_in_bookmart(self.order_items)
                voice = '즐겨찾기로 설정했어요'
                mv.make_voice(voice)
                chat.cm.write_chat(chat.chat('ai', voice))
        except Exception as e:
            err.write(e, '주문검색 끝에러')
            mv.playsound(sound_path+'something_wrong.mp3')

        finally:
            self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함
            self.order_items = []  # 장바구니에 담은 거 초기화

    def 가장최근구매상품주문(self):

        chat.cm.write_chat(chat.chat('ai', '가장 최근에 구매한 상품들을 주문하겠습니다.'))
        mv.playsound(sound_path + 'dorder_recent_products.mp3')
        history = ph.get_history()

        keys = list(history.keys())
        # 날짜를 기준으로 내림차순 정렬
        sorted_date_list = sorted(keys, key=lambda date_str: datetime.strptime(date_str, "%m월 %d일"), reverse=True)

        # history로부터 가장 최근 상품 가져오기
        recent_purchases_info = history[sorted_date_list[0]]

        voice = '가장 최근에 주문하신 상품이\n'
        # 주문할 상품 세팅
        items = []
        for item in recent_purchases_info:
            voice += f'{item["name"]}의 {item["quantity"]}개\n'
            items.append(buy.item(link=item['link'], quantity=item['quantity']))

        voice += '맞으십니까? 예 아니오로 말해주세요'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)
        mv.playsound(sound_path + 'water_drop.mp3')
        chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

        res = lc.listen(3)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        if '예' in res:
            chat.cm.write_chat(chat.chat('ai', '구매를 시작합니다. 잠시만 기다려주세요'))
            mv.playsound(sound_path + 'start_order.mp3')
            # 주문
            self.selen = buy.buyBySelenium()
            self.selen.go_to_mall()  # 홈페이지 이동
            self.selen.login()  # 홈페이지 로그인
            for item in items:
                self.selen.go_to_add_cart(item)

            chat.cm.write_chat(chat.chat('ai', "요청하신 상품을 장바구니에 모두 담았습니다"))
            mv.playsound(sound_path + 'request_item_all_clear.mp3')
            self.stage = 'call_ai'
            return

        chat.cm.write_chat(chat.chat('client', '주문을 취소합니다'))
        mv.playsound(sound_path + 'cancel_order.mp3')
        self.stage = 'call_ai'

    def 특정일구매상품주문(self):
        history = ph.get_history()
        for k in history:
            # print(k)
            if k in self.order:
                # history로부터 상품 목록 가져오기
                purchases_info = history[k]
                # 주문할 상품 세팅
                items = []
                for item in purchases_info:
                    items.append(buy.item(link=item['link'], quantity=item['quantity']))

                # 주문
                self.selen = buy.buyBySelenium()
                self.selen.go_to_mall()  # 홈페이지 이동
                self.selen.login()  # 홈페이지 로그인
                for item in items:
                    self.selen.go_to_add_cart(item)

                self.stage = 'call_ai'
                return

        # 말씀하신 구매날짜가 없습니다. 안내

        self.stage = 'call_ai'

    def 즐겨찾기구매(self):
        bookmark = ph.get_bookmark()
        voice = '원하시는 즐겨찾기의 상품이\n'
        # 주문할 상품 세팅
        items = []
        for item in bookmark:
            voice += f'{item["name"]}의 {item["quantity"]}개\n'
            items.append(buy.item(link=item['link'], quantity=item['quantity']))

        voice += '맞으십니까? 예 아니오로 말해주세요'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)
        mv.playsound(sound_path + 'water_drop.mp3')
        chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))

        res = lc.listen(3)  # 주문에 대한 확인 음성 받기
        chat.cm.write_chat(chat.chat('client', res))

        if '예' in res:
            chat.cm.write_chat(chat.chat('ai', '구매를 시작합니다. 잠시만 기다려주세요'))
            mv.playsound(sound_path + 'start_order.mp3')
            # 주문
            self.selen = buy.buyBySelenium()
            self.selen.go_to_mall()  # 홈페이지 이동
            self.selen.login()  # 홈페이지 로그인
            for item in items:
                self.selen.go_to_add_cart(item)

            chat.cm.write_chat(chat.chat('ai', "요청하신 상품을 장바구니에 모두 담았습니다"))
            mv.playsound(sound_path + 'request_item_all_clear.mp3')
            self.stage = 'call_ai'
            return

        chat.cm.write_chat(chat.chat('client', '주문을 취소합니다'))
        mv.playsound(sound_path + 'cancel_order.mp3')
        self.stage = 'call_ai'
