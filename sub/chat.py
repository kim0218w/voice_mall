import json
import os


class chat:
    def __init__(self, sender: str, text: str):
        self.sender = sender
        self.text = text


class chat_manager:

    file_path = './monitoring/chat.json'

    def write_chat(self, chat: chat):

        if os.path.exists(self.file_path):
            try:
                # 읽기 모드로 엶
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    chats = json.load(file)
                    new_data = {
                        'sender': chat.sender,
                        'text': chat.text
                    }

                    # 새로운 chat 업데이트
                    chats['messages'].append(new_data)

                # 다시 써주기
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(chats, file, ensure_ascii=False, indent=4)

            except Exception as e:
                print("chat-", e)

        else:
            try:
                # messages 담는 객체 생성
                chats = {
                    "messages": []
                }

                # message 넣어주기
                chats['messages'].append(
                    {
                        'sender': chat.sender,
                        'text': chat.text
                    }
                )
                # 데이터 json 파일에 써주기
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(chats, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print("chat-", e)

    def chat_room_init(self):
        # 파일이 존재하는지 확인
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                print(f"파일 {'order_confirm.mp3'} 이(가) 삭제되었습니다.")
            except Exception as e:
                print(f"파일 삭제 중 오류 발생: {e}")
        else:
            print(f"파일 {'order_confirm.mp3'} 이(가) 존재하지 않습니다.")


cm = chat_manager()
