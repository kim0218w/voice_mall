import sub.work_flow as wf
from dotenv import load_dotenv
import sub.chat as chat


def main():
    # 작업 흐름 제어 하는 객체
    wf_ctr = wf.controller()
    chat.cm.chat_room_init()
    while True:

        try:
            stage_func = wf_ctr.recognize_voice_interface()
            stage_func()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # .env 파일 로드하기
    load_dotenv()
    main()
