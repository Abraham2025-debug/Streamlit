import os
import subprocess
import sys
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from pydub import AudioSegment
import speech_recognition as sr

# Ensure ffmpeg is available
subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python-headless", "numpy", "Pillow", "SpeechRecognition", "pydub"], check=True)

# Define the directory for storing annotations
ANNOTATION_DIR = "annotations"
if not os.path.exists(ANNOTATION_DIR):
    os.makedirs(ANNOTATION_DIR)

st.write(f"Annotations will be stored in: `{ANNOTATION_DIR}`")

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
    try:
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
    except Exception as e:
        st.error(f"Error extracting frames: {e}")

    # Extract audio using ffmpeg and convert to .wav
    try:
        audio_path = "temp_audio.wav"  # Path to the extracted audio file

        # Extract audio using ffmpeg (no need for moviepy)
        subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path])

        # Now load the audio with pydub
        if os.path.exists(audio_path):  # Check if the audio file exists
            audio = AudioSegment.from_file(audio_path)

            # Perform speech recognition on the extracted audio
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
        else:
            st.write(f"Error: Audio file {audio_path} not found!")
    except Exception as e:
        st.error(f"Error processing video or audio: {e}")

st.write("Annotation tool is ready!")
