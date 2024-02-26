import streamlit as st
import numpy as np
import cv2
from PIL import Image
import webcolors
from gtts import gTTS
import os

def rgb_to_name(rgb):
    try:
        color_name = webcolors.rgb_to_name(rgb)
    except ValueError:
        color_name = "Unknown"
    return color_name

def detect_colors(image):
    # Convert image to OpenCV format (BGR)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Reshape image to a list of pixels
    pixels = image_bgr.reshape((-1, 3))

    # Convert to floating-point data type
    pixels = np.float32(pixels)

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)

    # Map the labels to the centers
    segmented_image = centers[labels.flatten()]

    # Reshape back to the original image shape
    segmented_image = segmented_image.reshape(image_bgr.shape)

    # Convert back to RGB format
    segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

    # Get the dominant colors
    dominant_colors = centers.tolist()
    color_names = [rgb_to_name(tuple(color)) for color in dominant_colors]

    return segmented_image_rgb, color_names

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")

def main():
    st.title("Color Detection Streamlit App")
    
    # File upload widget with multiple file types
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform Color Detection
        if st.button("Detect Colors"):
            # Convert PIL Image to NumPy array
            image_np = np.array(image)

            # Detect colors using the detect_colors function
            color_detected_image, color_names = detect_colors(image_np)

            # Display the color-detected image
            st.subheader("Color Detection Result:")
            st.image(color_detected_image, caption="Color Detection", use_column_width=True, channels="RGB")

            # Display the detected colors
            st.subheader("Detected Colors:")
            st.write(color_names)

            # Convert color names to a single string
            color_names_str = ", ".join(color_names)

            # Text-to-speech
            if st.button("Read Detected Colors"):
                text_to_speech(f"The detected colors are: {color_names_str}")

if __name__ == "__main__":
    main()
