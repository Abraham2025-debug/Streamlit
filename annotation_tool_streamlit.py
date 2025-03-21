import streamlit as st
import cv2
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from pathlib import Path
from streamlit_player import st_player

# Initialize app
st.title("Multimodal Sarcasm Annotation Tool")

# Sidebar for uploads
st.sidebar.header("Upload Files")
video_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
audio_file = st.sidebar.file_uploader("Upload Audio", type=["wav", "mp3"])
transcript_file = st.sidebar.file_uploader("Upload Transcript", type=["txt"])
frame_folder = st.sidebar.file_uploader("Upload Extracted Frames (Folder as .zip)", type=["zip"])

if video_file and audio_file and transcript_file and frame_folder:
    # Video playback
    st.subheader("Video Preview:")
    st.video(video_file)

    # Load transcript
    transcript = transcript_file.read().decode("utf-8").splitlines()
    st.subheader("Transcript:")
    st.text("\n".join(transcript))

    # Load audio and visualize waveform
    y, sr = librosa.load(audio_file)
    st.subheader("Audio Waveform:")
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)

    # Extract frames from the zip folder
    import zipfile
    with zipfile.ZipFile(frame_folder, 'r') as z:
        z.extractall("frames/")

    frame_files = sorted(list(Path("frames").glob("*.png")))
    st.subheader("Extracted Frames:")

    # Display frames with timestamp selection
    frame_annotations = {}
    for i, frame in enumerate(frame_files):
        st.image(str(frame), caption=f"Frame {i + 1}")
        sarcasm_label = st.selectbox(
            f"Annotate Frame {i + 1}", ["Select Label", "Sarcastic", "Non-Sarcastic"], key=f"frame_{i}")
        frame_annotations[str(frame)] = sarcasm_label

    # Save annotations
    if st.button("Save Annotations"):
        annotations = {
            "transcript": transcript,
            "frame_annotations": frame_annotations
        }
        with open("annotations.json", "w") as f:
            json.dump(annotations, f, indent=4)
        st.success("Annotations saved to annotations.json!")

