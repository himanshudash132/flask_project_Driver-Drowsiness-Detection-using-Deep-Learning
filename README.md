# Drowsiness Detection System

This project implements a real-time drowsiness detection system using a deep learning model. The system captures video from a webcam, detects faces and eyes, and uses a trained model to predict whether the user's eyes are open or closed. If the eyes are detected as closed for too long, an alarm sound is triggered to alert the user.

## Features

- **Real-Time Video Feed**: Capture video feed from a webcam and display it in real-time.
- **Face and Eye Detection**: Detects faces and eyes using Haar cascades.
- **Drowsiness Detection**: Predicts if the eyes are open or closed using a trained deep learning model.
- **Alarm System**: Triggers an alarm if the eyes remain closed for too long, indicating drowsiness.
- **Analytics Dashboard**: Displays real-time analytics including uptime, alert count, and average detection score.

## Demo

<!-- Add a link to the demo or a gif showcasing the project -->

## Installation

### Prerequisites

- Python 3.x
- TensorFlow
- OpenCV
- Pygame (for sound alarm)
- Flask

### Clone the Repository

```bash
git clone https://github.com/yourusername/drowsiness-detection.git
cd drowsiness-detection
```

### Install Dependencies
pip install -r requirements.txt
