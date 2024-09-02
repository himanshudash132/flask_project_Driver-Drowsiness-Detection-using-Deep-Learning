# # python app.py
# pip install Flask opencv-python-headless tensorflow numpy pygame
import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
from flask import Flask, Response, render_template, request, jsonify
import time

app = Flask(__name__)

# Load the face and eye detection models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Load the drowsiness detection model
model_path = os.path.join("models", "model.h5")
model = load_model(model_path)

# Global variables to manage video capture and analytics
cap = None
alert_count = 0
detection_scores = []
start_time = time.time()

def detect_drowsiness(frame):
    global alert_count, detection_scores
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, minNeighbors=3, scaleFactor=1.1, minSize=(25, 25))
    
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, minNeighbors=5, scaleFactor=1.1, minSize=(15, 15))
        
        for (ex, ey, ew, eh) in eyes:
            # Draw rectangle around the eyes
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
            # Preprocess the eye region for prediction
            eye = roi_color[ey:ey + eh, ex:ex + ew]
            eye = cv2.resize(eye, (80, 80))
            eye = eye / 255.0
            eye = eye.reshape(1, 80, 80, 3)
            
            # Predict drowsiness
            prediction = model.predict(eye)
            
            if prediction[0][0] > 0.30:
                cv2.putText(frame, "Closed", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                alert_count += 1
                detection_scores.append(1)  # Add a score for a closed eye detection
            elif prediction[0][1] > 0.70:
                cv2.putText(frame, "Open", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                detection_scores.append(0)  # Add a score for an open eye detection
    
    return frame

def gen_frames():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not start video capture")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Process the frame for drowsiness detection
        frame = detect_drowsiness(frame)
        
        # Encode the frame to JPEG
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

@app.route('/analytics_data')
def analytics_data():
    global alert_count, detection_scores, start_time
    uptime = time.time() - start_time
    avg_score = sum(detection_scores) / len(detection_scores) if detection_scores else 0
    return jsonify({
        'uptime': uptime,
        'alert_count': alert_count,
        'average_score': avg_score
    })

@app.route('/stop_video', methods=['POST'])
def stop_video():
    global cap
    if cap is not None:
        cap.release()
        cap = None
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    app.run(debug=True)



