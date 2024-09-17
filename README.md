# Driver Drowsiness Detection System

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
```bash
pip install -r requirements.txt
```
### Download Model
Place the trained model file (model.h5) in the models/ directory.

### Run the Application
```bash
python app.py
```
### Access the Application
Open your browser and go to http://127.0.0.1:5000/.

### Project Structure
```bash
your_project/
│
├── app.py                # Main Flask application
├── models/
│   └── model.h5          # Trained drowsiness detection model
├── static/
│   ├── alarm.wav         # Alarm sound file
│   ├── css/
│   │   └── styles.css    # CSS for styling the web application
│   └── js/
│       └── script.js     # JavaScript for real-time analytics
├── templates/
│   └── index.html        # HTML template for the web application
├── requirements.txt      # Python dependencies
└── README.md             # Project README file
```
### Usage
Start the Flask App: Run the application using the command python app.py.
Web Interface: Access the real-time video feed and analytics via the web interface at http://127.0.0.1:5000/.
Alarm System: The system will automatically trigger an alarm if it detects drowsiness.
### Screenshots
Real-Time Video Feed
  ![Real-Time Video Feed](https://github.com/himanshudash132/flask_project_Driver-Drowsiness-Detection-using-Deep-Learning/blob/main/image%20results/1.png)
  
Analytics Dashboard
  ![Real-Time Video Feed-Screenshot](https://github.com/himanshudash132/flask_project_Driver-Drowsiness-Detection-using-Deep-Learning/blob/main/image%20results/2.png)
### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgements
OpenCV
TensorFlow
Flask
Pygame
