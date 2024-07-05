import check_info as ci
import buy
import voice_recg as vr 

def main():
   
    
    order_processor = vr.OrderProcessor()
    id = 'beno10n@naver.com'
    pw = 'beco025yh'
    while True:
        try:
            products, bool = order_processor.run()
            if bool:
                go_to_mall = buy.buyBySelenium()
                go_to_mall.getUserInfo(id,pw)
                go_to_mall.login()
                go_to_mall.searchItem(products)
        except Exception as e:
            print(e)

        

    

if __name__ == '__main__':
    main()
   



