import os
import subprocess
import sys
import streamlit as st
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

# Ensure dependencies are installed
subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python-headless", "numpy", "Pillow", "SpeechRecognition", "moviepy", "pydub"], check=True)

# Define the directory for storing annotations
ANNOTATION_DIR = "annotations"

# Create the directory if it doesn't exist
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
        import cv2
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

    # Extract audio using MoviePy and convert to .wav
    try:
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"  # Path to the extracted audio file
        video.audio.write_audiofile(audio_path)

        # Now load the audio with pydub
        if os.path.exists(audio_path):  # Check if the audio file exists
            audio = AudioSegment.from_file(audio_path)

            # Perform speech recognition on the extracted audio
            import speech_recognition as sr
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
