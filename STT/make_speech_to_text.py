import requests
import os


class make_speech_to_text:

    # 환경변수 가져오기
    __client_id = os.getenv('STT_NAVER_CLOUD_CLIENT_ID')
    __client_secret = os.getenv('STT_NAVER_CLOUD_SECRET')
    __lang = "Kor"  # 언어 코드 ( Kor, Jpn, Eng, Chn )
    __url = os.getenv('STT_NAVER_CLOUD_URL') + __lang

    __headers = {
        "X-NCP-APIGW-API-KEY-ID": __client_id,
        "X-NCP-APIGW-API-KEY": __client_secret,
        "Content-Type": "application/octet-stream"
    }

    def make(self):
        try:
            data = open('client_voice.wav', 'rb')
            response = requests.post(
                self.__url,  data=data, headers=self.__headers)

            rescode = response.status_code
            if (rescode == 200):
                # print(response.text)
                return response.text
            else:
                raise Exception

        except Exception as e:
            print(e)


# test code
# mst = make_speech_to_text()
# mst.make()
