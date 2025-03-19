import streamlit as st
import os
import subprocess
import sys

# Ensure moviepy and other dependencies are installed
subprocess.run([sys.executable, "-m", "pip", "install", "moviepy", "opencv-python", "numpy", "Pillow", "SpeechRecognition"], check=True)

# Define the directory for storing annotations
ANNOTATION_DIR = "annotations"

# Create the directory if it doesn't exist
if not os.path.exists(ANNOTATION_DIR):
    os.makedirs(ANNOTATION_DIR)

st.write(f"Annotations will be stored in: `{ANNOTATION_DIR}`")

# Import necessary libraries after ensuring dependencies are installed
import cv2
import numpy as np
from PIL import Image
from moviepy import editor as mp
import speech_recognition as sr

# Streamlit App
st.title("Multimodal Sarcasm Annotation Tool")

# Upload video file
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)

    # Save uploaded file
    video_path = os.path.join("temp_video.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Use getbuffer() for better performance

    # Extract frames using OpenCV
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frame_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_list.append(frame)
        frame_count += 1

    cap.release()
    st.write(f"Total Frames Extracted: {frame_count}")

    # Display first frame as an example
    if frame_list:
        frame_rgb = cv2.cvtColor(frame_list[0], cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        st.image(image, caption="First Frame Extracted")

    # Extract audio using MoviePy
    try:
        video = mp.VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
                st.write("Transcription:", transcript)
            except sr.UnknownValueError:
                st.write("Could not understand the audio")
            except sr.RequestError as e:
                st.write(f"Error with speech recognition service: {e}")
    except Exception as e:
        st.write(f"Error processing video or audio: {e}")

st.write("Annotation tool is ready!")
