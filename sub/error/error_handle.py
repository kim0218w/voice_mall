from datetime import datetime
import os


class error:

    file_path = './sub/error/error.log'

    def write(self, err: Exception, msg: str):
        if os.path.exists(error.file_path):
            try:
                with open(error.file_path, 'a', encoding='utf-8') as file:
                    now = datetime.now()
                    file.write(f'{now.year}y {now.month}m {now.day}d {now.hour}h {now.minute} {now.second} {err}, {msg}\n')
            except Exception as e:
                print("log 파일 안 열림")
