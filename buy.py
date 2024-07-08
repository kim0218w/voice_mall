
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# 여기에 나머지 코드 추가

import time

class buyBySelenium:

    driver = None
    user_ID = None
    user_PW = None
    
    def __init__(self):
        pass

    # user 정보 받기
    def getUserInfo(self,id,pw):
        self.user_ID = id
        self.user_PW = pw

    # 홈페이지 접속 및 로그인
    def login(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # 크롤링 방지 설정을 undefined로 변경.: 추가
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                    """
        })
        
        # 쿠팡 홈페이지로 이동
        self.driver.get('https://www.coupang.com/')
        
        time.sleep(3)
        # 로그인 페이지로 이동
        login_button = self.driver.find_element(By.CSS_SELECTOR, '#login a')
        print(login_button)
        login_button.click()
        print()
        # 로그인 정보 입력
        time.sleep(3)  # 페이지 로딩 대기
        username = self.driver.find_element(By.ID, 'login-email-input')
        password = self.driver.find_element(By.ID, 'login-password-input')
        username.send_keys(self.user_ID)
        password.send_keys(self.user_PW)
        
        # 로그인 버튼 클릭
        login_button = self.driver.find_element(By.CSS_SELECTOR, '.login__button--submit-rds')
        login_button.click()
        
        # 로그인 완료될 때까지 잠시 대기
        time.sleep(5)
        
    # main에서 반복 돌릴거임. 여기서는 객체 하나만 받아서 동작하게 만들어라 규정아
    # 상품 검색 / 이름을 받아서 검색만 하도록 바꾸기
    
    def searchItem(self, product):
        
        # products => [{"item": 검색어, "quantity":수량}]
        # product =>
        # 상품 검색
        search_box = self.driver.find_element(By.CSS_SELECTOR, '#headerSearchKeyword')
        
        print(product)
        name = product['item']
        print(name)
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN) # 딱 여기까지 동작하게
        
    # 상품 목록에서 아이템 선택
    def choiceItem(self):
        # 상품 목록이 정상적으로 검색됐다 가정하고 동작
        # 상품 목록 가져오기
        shopping_products = self.driver.find_elements(By.XPATH, '//ul[@id="productList"]/li')
        
        # 상품 이름과 링크 추출
        product_list = []
        for shopping_product in shopping_products:
            name_element = shopping_product.find_element(By.XPATH, './/div[contains(@class, "name")]')
            link_element = shopping_product.find_element(By.XPATH, './/a')
            product_name = name_element.text
            product_link = link_element.get_attribute('href')
            product_list.append({'name': product_name, 'link': product_link})
        
        # 추출된 상품 목록 출력
        for idx, product in enumerate(product_list, start=1):
            print(f"{idx}. {product['name']}: {product['link']}")
        
        # 원하는 상품 선택 (여기서는 첫 번째 상품 선택 예시)
        selected_product = product_list[0]
        self.driver.get(selected_product['link']) # 하는것까지 
        
        # 상품 페이지 로딩 대기
        time.sleep(3)
        
        #--------------------------여기 list 맞춰서 수정해야함
        # item_quantity = item['quantity']
    
    # 상품 갯수만큼 장바구니에 담기
    def selectItem(self, quantity):
        try:
            prod_quantity = self.driver.find_element(By.CSS_SELECTOR, ".prod-quantity__plus")
            for i in range(quantity):
                prod_quantity.click()
        except Exception as e:
            print(e)
        #--------------------------
        
        # 장바구니에 담기 버튼 클릭
        add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, '.prod-cart-btn')
        add_to_cart_button.click()
        
        # 장바구니에 추가 완료될 때까지 잠시 대기
        time.sleep(5)

    #장바구니로 이동
    def cart(self):
        # browse_cart selector로 수정해야함
        browse_cart = self.driver.find_element(By.CSS_SELECTOR, '#header > section > div.clearFix.search-form-wrap > ul > li.cart.more > a > span.cart-icon.gnb-icon-item')
        browse_cart.click()
        time.sleep(10)




# 객체 생성 
id = 'cz18117@naver.com'
pw = '1q2w3e4r!@'
go_to_mall_obj = buyBySelenium()
go_to_mall_obj.getUserInfo(id,pw)
go_to_mall_obj.login()
go_to_mall_obj.cart()
# 브라우저 종료
# self.driver.quit()