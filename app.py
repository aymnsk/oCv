import streamlit as st
from backend import process_camera, text_to_speech

st.title("📷 CamCom - Gesture & Sign Language AI")

# Create placeholders for video feed and gesture output
video_placeholder = st.empty()
gesture_text_placeholder = st.empty()

st.sidebar.title("🔧 Options")

# Toggle states
if "gesture_ai" not in st.session_state:
    st.session_state.gesture_ai = False

if "sign_ai" not in st.session_state:
    st.session_state.sign_ai = False

# Toggle Gesture AI
if st.sidebar.button("Toggle Gesture AI"):
    st.session_state.gesture_ai = not st.session_state.gesture_ai

# Toggle Sign Language AI
if st.sidebar.button("Toggle Sign Language AI"):
    st.session_state.sign_ai = not st.session_state.sign_ai

st.write("🎥 Camera is ON")

# Run the camera in the background
frame_generator = process_camera(st.session_state.gesture_ai, st.session_state.sign_ai)

for frame_bytes, detected_sign in frame_generator:
    # Show live camera feed
    video_placeholder.image(frame_bytes, channels="BGR")

    # If Sign AI is enabled and sign is detected
    if st.session_state.sign_ai:
        if detected_sign:
            gesture_text_placeholder.write(f"🖐 Detected Sign: **{detected_sign}**")
            text_to_speech(detected_sign)
        else:
            gesture_text_placeholder.write("❌ No sign detected. Try again.")
