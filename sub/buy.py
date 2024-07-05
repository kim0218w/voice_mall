
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
    @classmethod
    def getUserInfo(cls,id,pw):
        cls.user_ID = id
        cls.user_PW = pw

    # 홈페이지 접속 및 로그인
    @classmethod
    def login(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # 크롤링 방지 설정을 undefined로 변경.: 추가
        cls.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                    """
        })
        
        # 쿠팡 홈페이지로 이동
        cls.driver.get('https://www.coupang.com/')
        
        time.sleep(3)
        # 로그인 페이지로 이동
        login_button = cls.driver.find_element(By.CSS_SELECTOR, '#login a')
        print(login_button)
        login_button.click()
        
        # 로그인 정보 입력
        time.sleep(3)  # 페이지 로딩 대기
        username = cls.driver.find_element(By.ID, 'login-email-input')
        password = cls.driver.find_element(By.ID, 'login-password-input')
        username.send_keys(cls.user_ID)
        password.send_keys(cls.user_PW)
        
        # 로그인 버튼 클릭
        login_button = cls.driver.find_element(By.CSS_SELECTOR, '.login__button--submit-rds')
        login_button.click()
        
        # 로그인 완료될 때까지 잠시 대기
        time.sleep(10)

    # 상품 목록에 따른 상품 정보 검색 및 장바구니 추가
    @classmethod
    def searchItem(self, products):
        
        print(products)
        for product in products:
            # products => [{"item": 검색어, "quantity":수량}]
            print(products)
            # 상품 검색
            search_box = self.driver.find_element(By.CSS_SELECTOR, '#headerSearchKeyword')
            
            #-------------------------여기 list 맞춰서 수정해야함
            # search_item = item['name']
            print(product)
            name = product['item']
            quantity = int(product['quantity'])
            print(name, quantity)
            search_box.send_keys(name)

            search_box.send_keys(Keys.RETURN)
            #-------------------------
            
            # 검색 결과 페이지 로딩 대기 
            time.sleep(3)
            
            # 상품 목록 가져오기
            products = self.driver.find_elements(By.XPATH, '//ul[@id="productList"]/li')
            
            # 상품 이름과 링크 추출
            product_list = []
            for product in products:
                name_element = product.find_element(By.XPATH, './/div[contains(@class, "name")]')
                link_element = product.find_element(By.XPATH, './/a')
                product_name = name_element.text
                product_link = link_element.get_attribute('href')
                product_list.append({'name': product_name, 'link': product_link})
            
            # 추출된 상품 목록 출력
            for idx, product in enumerate(product_list, start=1):
                print(f"{idx}. {product['name']}: {product['link']}")
            
            # 원하는 상품 선택 (여기서는 첫 번째 상품 선택 예시)
            selected_product = product_list[0]
            self.driver.get(selected_product['link'])
            
            # 상품 페이지 로딩 대기
            time.sleep(3)
            
            #--------------------------여기 list 맞춰서 수정해야함
            # item_quantity = item['quantity']
            

            try:
                prod_quantity = self.driver.find_element(By.CSS_SELECTOR, ".prod-quantity__plus")
                for i in range(quantity-1):
                    prod_quantity.click()
            except Exception as e:
                print(e)
            #--------------------------
            
            # 장바구니에 담기 버튼 클릭 (적절한 XPATH 수정 필요)
            add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, '.prod-cart-btn')
            add_to_cart_button.click()
            
            # 장바구니에 추가 완료될 때까지 잠시 대기
            time.sleep(5)

    @classmethod
    def cart(cls):
        # 장바구니로 이동
        browse_cart = cls.driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/header/section/div[1]/ul/li[2]/a/span[1]/img')
        browse_cart.click()
        time.sleep(10)



# 객체 생성 
# go_to_mall_obj = buyBySelenium()

# 브라우저 종료
# self.driver.quit()
