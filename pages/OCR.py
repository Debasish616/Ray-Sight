from PIL import Image
import streamlit as st
import pytesseract
import numpy as np
from gtts import gTTS
import os

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def ocr_image(image):
    text = pytesseract.image_to_string(image)
    return text

def save_text_to_file(text):
    with open("ocr_result.txt", "w") as file:
        file.write(text)

def read_text_from_file():
    with open("ocr_result.txt", "r") as file:
        text = file.read()
    return text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")

def main():
    st.title("OCR Streamlit App")

    # File upload widget with multiple file types
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Placeholder for OCR result
    ocr_result_placeholder = st.empty()

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR
        if st.button("Run OCR"):
            text_result = ocr_image(np.array(image))
            st.subheader("OCR Result:")
            ocr_result_placeholder.write(text_result)  # Write result to the placeholder

            # Save text to file
            save_text_to_file(text_result)

    # Text-to-speech
    if st.button("Convert to Speech"):
        # Read text from file and convert to speech
        saved_text = read_text_from_file()
        text_to_speech(saved_text)

if __name__ == "__main__":
    main()
