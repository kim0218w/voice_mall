import speech_recognition as sr
import whisper
import time
import pandas as pd
import pyttsx3

# Whisper 모델 로드
model = whisper.load_model("medium")

# 음성 인식기 설정
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# TTS 엔진 설정
engine = pyttsx3.init()

# 한글 숫자와 대응하는 아라비아 숫자 매핑
num_map = {
    "하나": "1",
    "둘": "2",
    "셋": "3",
    "넷": "4",
    "다섯": "5",
    "여섯": "6",
    "일곱": "7",
    "여덟": "8",
    "아홉": "9",
    "열": "10"
}

# 주문 리스트
order_list = []

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    transcribed_text = result["text"]
    return replace_numbers(transcribed_text)

def replace_numbers(text):
    """텍스트에서 한글 숫자를 아라비아 숫자로 변환합니다."""
    for word, num in num_map.items():
        text = text.replace(word, num)
    return text

def listen_for_keyword(keyword):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"키워드 '{keyword}' 대기 중...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                recognized_text = recognizer.recognize_google(audio, language="ko-KR")
                if keyword in recognized_text.lower():
                    print(f"키워드 '{keyword}' 감지!")
                    return
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("API 요청 중 오류 발생")
                continue

def record_audio(duration=5):
    with microphone as source:
        print("녹음 중...")
        audio = recognizer.listen(source, timeout=duration)
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("녹음 완료")
        return "temp.wav"

def speak_text(text):
    """텍스트를 음성으로 출력합니다."""
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        listen_for_keyword("hello")
        audio_path = record_audio(duration=5)
        listen_for_keyword("주문")
        if audio_path:
            transcribed_text = transcribe_audio(audio_path)
            print("변환된 텍스트:", transcribed_text)

            # 주문 리스트에 추가
            order_list.append(transcribed_text)
            
            # 변환된 텍스트를 파일로 저장
            with open("transcription.txt", "a", newline='', encoding='utf-8') as f:
                f.write(transcribed_text + "\n")
            
            # Pandas를 사용하여 텍스트 파일을 띄어쓰기 단위로 슬라이싱
            with open("transcription.txt", "r", encoding='utf-8') as f:
                text = f.read()
            words = text.split()
            df = pd.DataFrame(words, columns=["Word"])
            df.to_csv("transcription_sliced.csv", index=False, encoding='utf-8')
            
            # 주문 내용을 음성으로 출력
            order_text = "현재 주문 목록은 다음과 같습니다: " + ", ".join(order_list)
            speak_text(order_text)
        
        # 3초 후 다시 대기 상태로
        time.sleep(3)

if __name__ == "__main__":
    main()
