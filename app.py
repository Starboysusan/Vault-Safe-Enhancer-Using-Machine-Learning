import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import datetime
import smtplib
import pygame
import time
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import logging
from io import BytesIO

# -----------------------------
# Suppress YOLO info logs
# -----------------------------
logging.getLogger("ultralytics").setLevel(logging.ERROR)

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -----------------------------
# Create evidence folder
# -----------------------------
os.makedirs("evidence_images", exist_ok=True)

# -----------------------------
# Load YOLO model
# -----------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# -----------------------------
# Email function
# -----------------------------
def send_email_with_image(frame):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"evidence_images/evidence_{timestamp}.jpg"
    cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    msg = EmailMessage()
    msg["Subject"] = "🚨 ALERT: Human Detected"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(f"""
🚨 SECURITY ALERT 🚨

Human detected in restricted area.

Time: {timestamp}

See attached evidence image.
""")

    with open(image_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="jpeg", filename=f"evidence_{timestamp}.jpg")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        st.success("✅ Email Sent Successfully!")
    except Exception as e:
        st.error(f"Email error: {e}")

# -----------------------------
# Alarm function
# -----------------------------
def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="YOLO Surveillance", layout="wide")

tabs = st.tabs(["Live Camera", "Captured Evidence"])

# -----------------------------
# Live Camera Tab
# -----------------------------
with tabs[0]:
    st.markdown("### 📍 Location: Central Prison – Block A – Camera 3")

    ip_camera_url = st.text_input("Enter IP Camera URL", key="camera_input")

    # Start / Stop buttons
    if "streaming" not in st.session_state:
        st.session_state.streaming = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Streaming"):
            st.session_state.streaming = True
    with col2:
        if st.button("Stop Streaming"):
            st.session_state.streaming = False

    stframe = st.empty()
    last_email_time = 0
    cooldown = 60  # seconds between alerts

    if st.session_state.streaming:
        cap = cv2.VideoCapture(ip_camera_url)
        if not cap.isOpened():
            st.error("Unable to connect to camera.")
        else:
            while st.session_state.streaming:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to grab frame.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model(frame_rgb)

                current_time = time.time()
                person_detected = False

                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        if cls == 0:  # Person
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            person_detected = True

                if person_detected and (current_time - last_email_time > cooldown):
                    play_alarm()
                    send_email_with_image(frame_rgb)
                    last_email_time = current_time

                stframe.image(frame_rgb, channels="RGB")
                time.sleep(0.03)
            cap.release()

# -----------------------------
# Captured Evidence Tab
# -----------------------------
with tabs[1]:
    st.markdown("### 📸 Captured Evidence Images")
    evidence_files = sorted(os.listdir("evidence_images"), reverse=True)

    if evidence_files:
        cols_per_row = 3
        for i in range(0, len(evidence_files), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, img_file in enumerate(evidence_files[i:i+cols_per_row]):
                img_path = f"evidence_images/{img_file}"
                img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

                # Show image in column
                with cols[j]:
                    st.image(img, caption=img_file, width=300)            
                    buf = BytesIO()
                    cv2.imwrite(buf, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                    st.download_button(
                        label="Download",
                        data=buf.getvalue(),
                        file_name=img_file,
                        mime="image/jpeg"
                    )
    else:
        st.info("No evidence images captured yet.")