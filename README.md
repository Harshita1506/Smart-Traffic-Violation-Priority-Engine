# Smart Traffic Violation Priority Engine | AI-Powered Emergency Response

A real-time AI dashboard for monitoring traffic violations and density.

## Features
- **Live Video Feed**: Processes traffic footage in real-time.
- **Simulation Mode**: Works even without a video file (generates dummy data).
- **Real-time Alerts**: Detects speeding, red light violations, and more.
- **Premium UI**: Dark mode with glassmorphism effects.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   ## Model & Video Files

YOLOv8 models and traffic videos are excluded from the repository
due to GitHub size limits.

To run the project:

1. Download YOLO models:
```bash
pip install ultralytics
yolo download model=yolov8n.pt


## Video File
To use a real video:
1. Create a folder named `assets`.
2. Place your video file named `traffic.mp4` inside it.
3. Restart the app.
