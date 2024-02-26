import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Streamlit app
st.title("Speech Recognition App")

# Function to perform speech recognition
def recognize_speech(timeout=5):
    st.text("Say something:")
    with sd.InputStream(callback=callback):
        recording = sd.rec(int(timeout * 44100), samplerate=44100, channels=1, dtype='int16')
        sd.wait()
        
        # Recognize speech
        try:
            audio_data = sr.AudioData(np.array(recording.flatten()).tobytes(), 44100, 2)
            text = recognizer.recognize_google(audio_data)
            st.text(f"You said: {text}")
        except sr.UnknownValueError:
            st.text("Could not understand audio")
        except sr.RequestError as e:
            st.text(f"Error with the speech recognition service; {e}")

# Callback function for audio stream
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    recognizer.adjust_for_ambient_noise(np.array(indata), duration=0.2)

# Main Streamlit app
recognize_button = st.button("Start Speech Recognition")

if recognize_button:
    recognize_speech(timeout=5)  # Adjust the timeout as needed
