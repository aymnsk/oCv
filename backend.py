import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
from gtts import gTTS

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Sign Language Dictionary
SIGN_DICT = {
    "A": [0, 0, 0, 0, 0],  # Fist
    "B": [1, 1, 1, 1, 1],  # Open Hand
    "C": [0, 1, 1, 1, 1],  # Thumb Folded
    "D": [0, 1, 0, 0, 0],  # Index Finger Up
    "E": [0, 0, 1, 1, 1]   # Three Fingers Up
}

# Recognize Sign Function
def recognize_sign(fingers):
    for letter, pattern in SIGN_DICT.items():
        if fingers == pattern:
            return letter
    return None  

# Function to process camera and detect gestures/signs
def process_camera(toggle_gesture, toggle_sign):
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        detected_sign = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y])

                # Gesture AI (Cursor Control)
                if toggle_gesture:
                    index_x, index_y = int(landmarks[8][0] * pyautogui.size()[0]), int(landmarks[8][1] * pyautogui.size()[1])
                    pyautogui.moveTo(index_x, index_y)

                # Sign Language AI - **Fixing Finger Detection**
                if toggle_sign:
                    thumb_open = 1 if landmarks[4][0] > landmarks[3][0] else 0
                    index_finger = 1 if landmarks[8][1] < landmarks[6][1] else 0
                    middle_finger = 1 if landmarks[12][1] < landmarks[10][1] else 0
                    ring_finger = 1 if landmarks[16][1] < landmarks[14][1] else 0
                    pinky_finger = 1 if landmarks[20][1] < landmarks[18][1] else 0

                    fingers = [thumb_open, index_finger, middle_finger, ring_finger, pinky_finger]
                    detected_sign = recognize_sign(fingers)

        # Encode frame for Streamlit display
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield frame_bytes, detected_sign

    cap.release()

# Convert detected sign to speech
def text_to_speech(detected_sign):
    if detected_sign:
        tts = gTTS(f"Detected sign is {detected_sign}")
        tts.save("output.mp3")
        os.system("mpg123 output.mp3")
