
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os
import sub.error.error_handle as error
err = error.error()

# for test code
# from dotenv import load_dotenv
# load_dotenv()


class item:
    name = ''
    price = ''
    arrival_info = ''
    link = ''

    def __init__(self, name='', price='', arrival_info='', link='', quantity=0):
        self.name = name
        self.price = price
        self.arrival_info = arrival_info
        self.link = link
        self.quantity = quantity


class buyBySelenium:

    __user_ID = os.getenv('COUPANG_ID')
    __user_PW = os.getenv('COUPANG_PW')

    def __init__(self):
        buyBySelenium.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

        # 크롤링 방지 설정을 undefined로 변경.: 추가
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        })
                        """
        })

    def go_to_mall(self):

        # 쿠팡 홈페이지로 이동
        self.driver.get('https://www.coupang.com/')
        time.sleep(3)

    # 홈페이지 접속 및 로그인
    @classmethod
    def login(self):
        # 로그인 페이지로 이동
        login_button = self.driver.find_element(By.CSS_SELECTOR, '#login a')
        # print(login_button)
        login_button.click()

        # 로그인 정보 입력
        time.sleep(5)  # 페이지 로딩 대기
        username = self.driver.find_element(By.ID, 'login-email-input')
        password = self.driver.find_element(By.ID, 'login-password-input')
        username.send_keys(self.__user_ID)
        password.send_keys(self.__user_PW)

        # 로그인 버튼 클릭
        login_button = self.driver.find_element(
            By.CSS_SELECTOR, '.login__button--submit-rds')
        login_button.click()

        # 로그인 완료될 때까지 잠시 대기
        time.sleep(10)

    # 검색창에 상품 검색
    def search_item(self, search_word):

        # 상품검색창 dom 가져오기
        search_box = self.driver.find_element(
            By.CSS_SELECTOR, '#headerSearchKeyword')

        # item.name으로 검색
        search_box.send_keys(search_word)
        search_box.send_keys(Keys.RETURN)

        # 검색 결과 페이지 로딩 대기
        time.sleep(3)

    # 페이지의 상품 추출하는 메서드
    def get_related_items(self) -> list:

        # 상품 목록 가져오기
        its = self.driver.find_elements(
            By.XPATH, '//ul[@id="productList"]/li')

        # print(its)
        # 상품 이름과 링크 추출
        item_list = []
        count = 0
        for it in its:

            # 첫 번째 상품 제거 (보통 추천상품임)
            if count == 0:
                count += 1
                continue

            if count > 3:  # 3개 뽑음
                break
            count += 1

            # 담는데 문제 있으면 그 상품 안 담음
            try:
                link_element = it.find_element(By.XPATH, './/a')
                it_link = link_element.get_attribute('href')
            except Exception as e:
                err.write(e, '')
                continue
            try:
                it_name = it.find_element(
                    By.XPATH, './/div[contains(@class, "name")]').text
            except Exception as e:
                err.write(e, '')
                continue
            try:
                it_price = it.find_element(
                    By.CSS_SELECTOR, '.price-value').text
            except Exception as e:
                err.write(e, '')
                continue
            try:
                it_arrive_time = it.find_element(
                    By.CSS_SELECTOR, '.arrival-info').text
            except Exception as e:
                err.write(e, '')
                continue

            item_list.append(
                item(it_name, it_price, it_arrive_time, it_link))
            # print(it_name)

        return item_list

    # 상품 페이지로 들어가 장바구니에 담는 메서드
    def go_to_add_cart(self, item: item):

        self.driver.get(item.link)

        # 상품 페이지 로딩 대기
        time.sleep(3)
        try:
            prod_quantity = self.driver.find_element(
                By.CSS_SELECTOR, ".prod-quantity__plus")
            # print(item.quantity)
            for i in range(item.quantity):
                prod_quantity.click()
        except Exception as e:
            err.write(e, "buy.py go_to_add_cart 에러")
            print(e)
            # --------------------------

            # 장바구니에 담기 버튼 클릭 (적절한 XPATH 수정 필요)
        add_to_cart_button = self.driver.find_element(
            By.CSS_SELECTOR, '.prod-cart-btn')
        add_to_cart_button.click()

        # 장바구니에 추가 완료될 때까지 잠시 대기
        time.sleep(5)

    # 상품 관련 품목
    # 상품 목록에 따른 상품 정보 검색 및 장바구니 추가

    @classmethod
    def cart(self):
        # 장바구니로 이동
        browse_cart = self.driver.find_element(
            By.CSS_SELECTOR, '#header > section > div.clearFix.search-form-wrap > ul > li.cart.more > a > span.cart-icon.gnb-icon-item')
        browse_cart.click()
        time.sleep(10)


# # 객체 생성
# go_to_mall_obj = buyBySelenium()
# go_to_mall_obj.go_to_mall()
# go_to_mall_obj.login()
# go_to_mall_obj.search_item(item("딸기"))
# go_to_mall_obj.go_to_add_cart(go_to_mall_obj.get_related_items()[0], 1)  # 맨 처음에 있는 딸기 하나 선택
# 브라우저 종료
# self.driver.quit()
