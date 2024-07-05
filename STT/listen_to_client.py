from STT import make_speech_to_text as mst
from STT import voice_recoder as vr
import json


class listen_to_client:
    def __init__(self):
        self.__vr = vr.voice_recorder()
        self.__mst = mst.make_speech_to_text()

    def listen(self, duration: int):
        self.__vr.record_audio(duration)
        result = self.__mst.make()
        voice_to_text = json.loads(result)
        # print(voice_to_text['text'])
        return voice_to_text['text']


# test code
# lc = listen_to_client()
# lc.listen(duration=10) # 녹음시간 10초
