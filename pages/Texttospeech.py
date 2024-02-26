import streamlit as st
import pyttsx3

def tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.save_to_file(text, 'output.mp3')  # Save the speech to a file
    engine.runAndWait()

if __name__ == "__main__":
    st.title("Text-to-Speech with pyttsx3")

    # Text input
    text_input = st.text_area("Enter text to convert to speech")

    # Button to trigger text-to-speech
    if st.button("Convert to Speech"):
        if text_input:
            # Perform text-to-speech conversion
            tts(text_input)

            # Provide a download link for the generated audio file
            st.audio('output.mp3', format="audio/mp3")
