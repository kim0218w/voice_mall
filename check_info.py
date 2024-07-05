class InvalidFormatError(Exception):
    pass
    

def read_credentials(file_path):
    try:
        with open(file_path, 'r') as file:

            lines = file.readlines()
           
            for line in lines:
                line = line.strip()  # Remove any leading/trailing whitespace
                # print(line)
                if line:  # Skip empty lines
                    user_id, password = line.split(':')

                    if user_id == '' or password =='':
                        print('아이디 또는 비밀번호가 유효하지 않습니다._read_credentials')
                        return '',''
                    return user_id,password
    except Exception as e:
        print('파일을 여는데 문제가 생긴 거 같습니다.')
        return '',''