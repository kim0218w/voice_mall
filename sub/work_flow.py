import sub.make_voice as mv
import sub.extractor as ex
import sub.buy as buy
import os
from STT import listen_to_client as ltc
import sub.chat as chat
import sub.history.purchase_history as ph
from datetime import datetime
import string
import sub.error.error_handle as error
err = error.error()

id = os.getenv('COUPANG_ID')
pw = os.getenv('COUPANG_PW')

lc = ltc.listen_to_client()
ai_name = '광태'
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
            'order_items_in_bookmark': self.즐겨찾기구매
        }
        # stage에 맞는 함수 반환
        return go_to_stage[self.stage]

    def ai호출(self):
        # ai 부르는 거 듣기
        call_ai = lc.listen(duration=5)
        print(call_ai)
        if ai_name in call_ai or '강태' in call_ai or '캉태' in call_ai or '광택' in call_ai or '강택' in call_ai or '과학대' in call_ai:
            chat.cm.write_chat(chat.chat('client', call_ai))
            self.order_items = []  # 장바구니에 담을 상품들 초기화
            # order stage로 이동
            self.stage = 'order_listen'

    def 주문듣기(self):
        chat.cm.write_chat(chat.chat('ai', '주문받는중'))
        mv.playsound(sound_path + 'water_drop.mp3')

        # 주문듣기 10초
        self.order = lc.listen(7)
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

        # 주문 확인 받기
        _, ok = self.__if_user_ok(voice)
        if ok:
            chat.cm.write_chat(chat.chat('ai', "쿠팡으로 이동합니다."))
            mv.playsound(sound_path + 'go_to_coupang.mp3')  # 주문중 안내
            self.stage = 'order_search'  # 주문검색
        else:
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
                voice = '상위 3개의 상품 중에\n'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)
                i = 1
                for item in items:
                    voice = f'{i}번. {item.name} {item.price}원, {ex.ProductQuantityExtractor().format_dates(item.arrival_info)}\n'
                    chat.cm.write_chat(chat.chat('ai', voice))
                    mv.make_voice(voice)
                    i += 1
                voice = '들이 있어요. 어떤 걸 고르시겠어요? 1번째 2번째 3번째로 말해주세요'
                ITEM_NUM, ok = self.__select_item_num(voice)
                if ok:
                    #### 수량 설정 ####
                    # 상품을 주문합니다. 몇 개를 주문하시겠어요?
                    voice = f'{ITEM_NUM}번째 상품을 주문합니다. 몇 개를 주문하시겠어요?'
                    ITEM_QUAN, ok = self.__get_quantity(voice)
                    if ok:
                        #### 최종 확인 ####
                        # 몇 번째 상품 + 수량 맞으십니까?
                        voice = f'{ITEM_NUM}번째 상품 {ITEM_QUAN}개 맞으십니까?'
                        _, ok = self.__if_user_ok(voice)
                        if ok:
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
                        else:
                            # 주문취소
                            mv.make_voice('주문이 담기지 않았어요 필요하시면 저를 다시 불러주세요')
                            self.stage = 'call_ai'
                            return
                    else:
                        # 주문취소
                        mv.make_voice('주문이 담기지 않았어요 필요하시면 저를 다시 불러주세요')
                        self.stage = 'call_ai'
                        return
                else:
                    # 주문취소
                    mv.make_voice('주문이 담기지 않았어요 필요하시면 저를 다시 불러주세요')
                    self.stage = 'call_ai'
                    return

            self.stage = 'order_add'  # 주문 추가 여부를 물어보러 이동
        except Exception as e:
            if len(self.order_items) != 0:
                mv.make_voice('주문이 되지 않은게 있어요. 나중에 추가해주세요')
                chat.cm.write_chat(chat.chat('ai', '주문이 되지 않은게 있어요. 나중에 추가해주세요'))
                self.stage = 'order_add'  # 주문 추가 여부를 물어보러 이동
            else:
                err.write(e, '주문검색 에러')
                chat.cm.write_chat(chat.chat('ai', '오류발생 다시 저를 불러주세요'))
                mv.playsound(sound_path+'something_wrong.mp3')
                self.stage = "call_ai"  # 다시 ai 호출을 기다리도록 함

    def 주문추가(self):
        # 추가하실 것이 더 있습니까?
        voice = '추가하실 것이 더 있으신가요?'
        _, ok = self.__if_user_ok(voice)
        if ok:
            # 추가주문해주세요
            chat.cm.write_chat(chat.chat('ai', "주문을 해주세요."))
            mv.playsound(sound_path + 'add_items_in_cart.mp3')
            self.stage = 'order_listen'  # 주문듣기로 이동
        else:
            # 장바구니로 이동합니다.
            self.stage = 'end'

    def 끝(self):

        try:
            # 요청하신 상품을 장바구니에 모두 담았습니다.
            chat.cm.write_chat(chat.chat('ai', "요청하신 상품을 장바구니에 모두 담았습니다"))
            mv.playsound(sound_path + 'request_item_all_clear.mp3')

            # 즐겨찾기 등록
            voice = '즐겨찾기로 설정할까요? 한 개만 저장할 수 있어요'

            _, ok = self.__if_user_ok(voice)
            if ok:
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
            chat.cm.write_chat(chat.chat('ai', '요청을 모두 완료했습니다. 다시 저를 불러주세요'))
            mv.make_voice('요청을 모두 완료했습니다. 제가 필요하시면 다시 불러주세요')
            chat.cm.write_chat(chat.chat('ai', './엄지척_광태.png'))

    def 가장최근구매상품주문(self):

        chat.cm.write_chat(chat.chat('ai', '가장 최근에 구매한 상품들을 주문하겠습니다.'))
        mv.playsound(sound_path + 'order_recent_products.mp3')
        history = ph.get_history()

        keys = list(history.keys())
        # 날짜를 기준으로 내림차순 정렬
        sorted_date_list = sorted(keys, key=lambda date_str: datetime.strptime(date_str, "%m월 %d일"), reverse=True)

        # history로부터 가장 최근 상품 가져오기
        recent_purchases_info = history[sorted_date_list[0]]

        voice = '가장 최근에 주문하신 상품이\n'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)
        # 주문할 상품 세팅
        items = []
        for item in recent_purchases_info:
            voice = f'{item["name"]}의 {item["quantity"]}개\n'
            chat.cm.write_chat(chat.chat('ai', voice))
            mv.make_voice(voice)
            items.append(buy.item(link=item['link'], quantity=item['quantity']))

        voice = '맞으십니까?'
        _, ok = self.__if_user_ok(voice)
        if ok:
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
            mv.make_voice('요청을 모두 완료했습니다. 제가 필요하시면 다시 불러주세요')
            chat.cm.write_chat(chat.chat('ai', './헤드셋_광태.jpg'))
        else:
            chat.cm.write_chat(chat.chat('client', '주문을 취소합니다'))
            mv.playsound(sound_path + 'cancel_order.mp3')
            self.stage = 'call_ai'

    def 즐겨찾기구매(self):
        bookmark = ph.get_bookmark()
        voice = '원하시는 즐겨찾기의 상품이\n'
        chat.cm.write_chat(chat.chat('ai', voice))
        mv.make_voice(voice)
        # 주문할 상품 세팅
        items = []
        for item in bookmark:
            voice = f'{item["name"]}의 {item["quantity"]}개\n'
            chat.cm.write_chat(chat.chat('ai', voice))
            mv.make_voice(voice)
            items.append(buy.item(link=item['link'], quantity=item['quantity']))

        voice = '맞으십니까?'
        _, ok = self.__if_user_ok(voice)
        if ok:
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
            mv.make_voice('요청을 모두 완료했습니다. 제가 필요하시면 다시 불러주세요')
            chat.cm.write_chat(chat.chat('ai', './ai_광태.png'))

        else:
            chat.cm.write_chat(chat.chat('client', '주문을 취소합니다'))
            mv.playsound(sound_path + 'cancel_order.mp3')

        self.stage = 'call_ai'

    # 유저가 동의하는지 확인하는 함수
    # (result:str, ok:bool) 반환
    def __if_user_ok(self, ai_question: str) -> tuple:

        count = 3  # 대답 횟수
        chat.cm.write_chat(chat.chat('ai', ai_question))
        mv.make_voice(ai_question)

        for _ in range(count):
            chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))
            mv.playsound(sound_path + 'water_drop.mp3')
            res = lc.listen(3)  # 음성 받기
            chat.cm.write_chat(chat.chat('client', res))
            # 긍정응답이면
            if self.__check_positive_response(res):
                return res, True
            elif '' != res and ('취소' in res or '아니' in res or '없' in res or '안' in res or '됐다'):
                return '-1', False
            else:
                voice = '유효하지 않는 답이에요 다시 말해주세요'
                chat.cm.write_chat(chat.chat('ai', voice))
                mv.make_voice(voice)

        return '', False

    # 몇 번째 상품을 고르는지 확인하는 함수
    def __select_item_num(self, ai_question: str) -> tuple:

        count = 3  # 대답 횟수
        chat.cm.write_chat(chat.chat('ai', ai_question))
        mv.make_voice(ai_question)

        for _ in range(count):
            chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))
            mv.playsound(sound_path + 'water_drop.mp3')
            res = lc.listen(3)  # 주문에 대한 확인 음성 받기
            chat.cm.write_chat(chat.chat('client', res))

            result = ex.ProductQuantityExtractor().selectNum(res)
            try:
                # print(result)
                return int(result), True
            except:
                if result == None:
                    voice = '유효하지 않는 답이에요 다시 말해주세요'
                    mv.make_voice(voice)
                    chat.cm.write_chat(chat.chat('ai', voice))
                elif '취소' in res or '아니' in res or '없' in res or '안' in res or '됐다':
                    return -1, False

        return 0, False

    def __get_quantity(self, ai_question: str) -> tuple:
        count = 3  # 대답 횟수
        chat.cm.write_chat(chat.chat('ai', ai_question))
        mv.make_voice(ai_question)

        for _ in range(count):
            chat.cm.write_chat(chat.chat('ai', '듣고 있어요'))
            mv.playsound(sound_path + 'water_drop.mp3')
            res = lc.listen(3)  # 주문에 대한 확인 음성 받기
            chat.cm.write_chat(chat.chat('client', res))

            result = ex.ProductQuantityExtractor().convert_korean_numbers(res)

            try:
                print(result)
                return int(result), True
            except Exception:
                if result == None:
                    voice = '유효하지 않는 답이에요 다시 말해주세요'
                    mv.make_voice(voice)
                    chat.cm.write_chat(chat.chat('ai', voice))
                elif '취소' in res or '아니' in res or '없' in res or '안' in res or '됐다':
                    return -1, False

        return 0, False

    # 긍정응답이면 True, 아니면 False 반환

    def __check_positive_response(self, user_input):
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
