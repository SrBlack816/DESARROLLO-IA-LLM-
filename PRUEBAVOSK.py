from vosk import Model, KaldiRecognizer
import pyaudio
import json

import os
print("📌 Ruta actual:", os.getcwd())

model = Model(r"C:\Users\N\Desktop\LAB INTELIGENCIA ARTIFICIAL\LAB 7\model-es")
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Habla ahora...")

while True:
    data = stream.read(160000, exception_on_overflow=False) # 160000 bytes = a 5 segundos de captura de datos
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)["text"]
        print("Transcripción:", text)
        break

stream.stop_stream()
stream.close()
p.terminate()