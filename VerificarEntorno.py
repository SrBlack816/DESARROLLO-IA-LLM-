import streamlit as st
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from langchain_community.llms import Ollama

# Inicialización del modelo de Llama3
llm = Ollama(model="llama3")

# Inicialización de Vosk
MODEL_PATH = "model-es"  # Asegúrate de que esta ruta sea correcta
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Configuración de PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

# Interfaz en Streamlit
st.title("Chatbot con Captura de Voz 🎙️🤖")

# Espacio para mostrar transcripción
text_area = st.empty()

# Botón para activar la captura
if st.button("🎙️ Iniciar Captura de Voz"):
    st.write("🔥 Capturando voz... habla ahora.")
    stream.start_stream()
    while True:
        data = stream.read(160000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            text_area.write(f"🗣️ Transcripción: {text}")
            break

    stream.stop_stream()
    st.success("✅ Captura finalizada.")
    
    if text:
        st.write("🤖 Generando respuesta con Llama3...")
        with st.spinner("Pensando..."):
            st.write_stream(llm.stream(text, stop=['<|eot_id|>']))
    
# Finalización del stream
stream.close()
p.terminate()