# # python app.py
# pip install Flask opencv-python-headless tensorflow numpy pygame
import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
from flask import Flask, Response, render_template, request, jsonify

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

model_path = os.path.join("models", "model.h5")
model = load_model(model_path)

# Global variable to manage video capture
cap = None

def detect_drowsiness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, minNeighbors=3, scaleFactor=1.1, minSize=(25, 25))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        for (ex, ey, ew, eh) in eyes:
            eye = frame[y + ey:y + ey + eh, x + ex:x + ex + ew]
            eye = cv2.resize(eye, (80, 80))
            eye = eye / 255.0
            eye = eye.reshape(1, 80, 80, 3)
            prediction = model.predict(eye)
            
            if prediction[0][0] > 0.30:
                cv2.putText(frame, "Closed", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            elif prediction[0][1] > 0.70:
                cv2.putText(frame, "Open", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
    
    return frame

def gen_frames():
    global cap
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        frame = detect_drowsiness(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video', methods=['POST'])
def stop_video():
    global cap
    if cap is not None:
        cap.release()
        cap = None
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    app.run(debug=True)
