from gtts import gTTS
from playsound import playsound
import os


def make_voice(text):
    file_name = 'order_confirm.mp3'
    tts_obj = gTTS(text, lang='ko')
    tts_obj.save(file_name)
    play_sound(file_name)
    # 파일이 존재하는지 확인
    if os.path.exists('order_confirm.mp3'):
        try:
            os.remove('order_confirm.mp3')
            print(f"파일 {'order_confirm.mp3'} 이(가) 삭제되었습니다.")
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {e}")
    else:
        print(f"파일 {'order_confirm.mp3'} 이(가) 존재하지 않습니다.")
        print(text)


def play_sound(file_name):
    playsound(file_name)
