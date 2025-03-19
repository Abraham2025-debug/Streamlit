import streamlit as st
import os
import subprocess
import sys

# Ensure dependencies are installed
subprocess.run([sys.executable, "-m", "pip", "install", "moviepy", "opencv-python-headless", "numpy", "Pillow", "SpeechRecognition"], check=True)

# Define the directory for storing annotations
ANNOTATION_DIR = "annotations"

# Create the directory if it doesn't exist
if not os.path.exists(ANNOTATION_DIR):
    os.makedirs(ANNOTATION_DIR)

st.write(f"Annotations will be stored in: `{ANNOTATION_DIR}`")

# Import necessary libraries after ensuring dependencies are installed
try:
    import cv2
    import numpy as np
    from PIL import Image
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip  # Corrected import
    import speech_recognition as sr
except ImportError as e:
   
