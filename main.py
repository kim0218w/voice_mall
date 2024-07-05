import check_info as ci
import buy
import voice_recg as vr 

def main():
   
    
    order_processor = vr.OrderProcessor()
    file_path = 'info.txt'
    id, pw = ci.read_credentials(file_path)
    if id == '' or pw == '':
        print('아이디 또는 비밀번호가 유효하지 않습니다.')
        return 
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
   



