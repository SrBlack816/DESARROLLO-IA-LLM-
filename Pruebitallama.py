import streamlit as st
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from langchain_community.llms import Ollama
import pyttsx3  # Librería para convertir texto en voz

# Inicialización del modelo de Llama3
llm = Ollama(model="llama3")

# Inicialización de Vosk
MODEL_PATH = r"C:\Users\N\Desktop\LAB INTELIGENCIA ARTIFICIAL\LAB 7\model-es"  # Ruta absoluta al modelo
model = Model(MODEL_PATH)

# Inicialización de pyttsx3 para la conversión de texto a voz
engine = pyttsx3.init()

# Interfaz en Streamlit
st.title("Chatbot con Captura de Voz 🎙️🤖")

# Elemento de Streamlit para mostrar la transcripción en tiempo real
text_area = st.empty()

# Botón para activar la captura
if st.button("🎙️ Iniciar Captura de Voz"):
    st.write("🔥 Capturando voz... habla ahora.")
    
    # Configuración de PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    recognizer = KaldiRecognizer(model, 16000)
    texto_completo = ""

    # Captura en tiempo real
    while True:
        data = stream.read(160000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text:
                texto_completo += text + " "
                st.write(f"**🗣️ Transcripción:** {texto_completo}")
                print(texto_completo)
            break

    # Cerrar streams
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    st.success("✅ Captura finalizada.")
    
    if texto_completo:
        st.write("🤖 Generando respuesta con Llama3...")

        
    with st.spinner("Pensando..."):
        # Creamos un contenedor vacío para ir actualizando el texto sin saltos de línea
        respuesta_container = st.empty()
        respuesta_completa = ""
    
    for fragmento in llm.stream(texto_completo, stop=['<|eot_id|>']):
        respuesta_completa += fragmento
        # Actualizamos el contenedor con el texto completo (sin salto de línea)
        respuesta_container.markdown(f"**🤖 Respuesta:** {respuesta_completa}")
        
        # Decir el fragmento en voz alta
        engine.say(fragmento)
        engine.runAndWait()