import pyaudio
import wave


class voice_recorder:
    def __init__(self):
        self.__filename = 'client_voice.wav'

    # 사람 목소리를 녹음하는 함수

    def record_audio(self, duration, sample_rate=44100, chunk_size=1024, channels=1):
        p = pyaudio.PyAudio()

        # 오디오 스트림 열기
        stream = p.open(format=pyaudio.paInt16,  # 16비트 정수형 샘플 형식
                        channels=channels,       # 오디오 채널 수 (1 = 모노, 2 = 스테레오)
                        rate=sample_rate,        # 샘플링 레이트 (초당 샘플 수)
                        input=True,              # 입력 스트림 (마이크로폰)
                        frames_per_buffer=chunk_size)  # 버퍼 당 프레임 수

        print("Recording...")
        frames = []

        # 녹음 루프
        for _ in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)  # 버퍼 크기만큼 데이터 읽기
            frames.append(data)  # 읽은 데이터를 프레임 리스트에 추가

        print("Recording finished.")

        # 스트림 정리
        stream.stop_stream()  # 스트림 정지
        stream.close()        # 스트림 닫기
        p.terminate()         # PyAudio 종료

        # WAV 파일로 저장
        wf = wave.open(self.__filename, 'wb')
        wf.setnchannels(channels)  # 채널 수 설정
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  # 샘플 너비 설정
        wf.setframerate(sample_rate)  # 샘플링 레이트 설정
        wf.writeframes(b''.join(frames))  # 프레임 데이터를 WAV 파일에 기록
        wf.close()  # 파일 닫기
        print(f"Saved WAV file: {self.__filename}")


# test code
# vr = voice_recorder()
# vr.record_audio(5)
