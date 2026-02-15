# ✋🤖  AI Rock Paper Scissors – YOLO + Arduino (Timed Match System)

A real-time Hand Gesture–Based Rock Paper Scissors Game powered by YOLOv8 object detection, OpenCV image processing, and an Arduino-controlled physical response system.

This project combines:

🔍 Deep Learning (YOLOv8)

🖼️ Computer Vision (OpenCV)

🎮 Game Logic & AI Strategy

🔌 Hardware Integration (Arduino)

⏱️ Timed Match System

🚀 Project Overview

The system detects a player's hand using YOLOv8, classifies the gesture using contour-based finger detection, and plays against the user in a 60-second timed match.

The AI system sends its move to an Arduino device via serial communication, enabling physical interaction (LEDs, display, servo, etc.).

# 🧠 How It Works
1️⃣ Hand Detection

YOLO detects the hand bounding box in real-time from webcam feed.

2️⃣ Gesture Classification

Inside the detected region:

Convert to grayscale

Apply Gaussian blur

Apply Otsu thresholding

Extract contours

Compute convex hull & convexity defects

Count fingers to classify:

ROCK

PAPER

SCISSORS

3️⃣ AI Decision Logic

The system always selects the winning counter move:

ROCK → AI plays PAPER

PAPER → AI plays SCISSORS

SCISSORS → AI plays ROCK

4️⃣ Arduino Communication

AI move is sent via serial communication:

arduino.write((ai_gesture + "\n").encode())


This allows hardware-based output (robotic arm, LEDs, display, etc.).

5️⃣ Timed Match System

60-second game duration

Real-time score tracking

Game over screen

Restart option (Press R)

🛠️ Technologies Used

🐍 Python 3.x

📷 OpenCV

🤖 Ultralytics YOLOv8

🔢 NumPy

🔌 PySerial

🕹️ Arduino

📂 Project Structure
AI-RPS-YOLO-Arduino/
│
├── hand_yolov8n.pt       # Custom trained YOLO model
├── main.py               # Game logic + detection + Arduino control
├── requirements.txt
└── README.md

# ▶️ Installation
1️⃣ Clone Repository
git clone https://github.com/yourusername/ai-rps-yolo-arduino.git
cd ai-rps-yolo-arduino

2️⃣ Install Dependencies
pip install ultralytics opencv-python numpy pyserial

3️⃣ Connect Arduino

Set correct COM port:

arduino = serial.Serial("COM3", 9600, timeout=1)


Change "COM3" if needed.

4️⃣ Run the Game
python main.py

# 🎮 Controls
Key	Action
ESC	Quit Game
R	Restart Match
📊 Game Features

Real-time YOLO detection

Finger counting gesture recognition

AI counter-move logic

Live scoreboard

60-second timed challenge

Hardware interaction

Game restart functionality

# 🔥 System Highlights

Combines Deep Learning + Classical CV

Real-time performance

Edge-device compatible

Hardware + AI integration

Interactive AI gaming system


# 🎯 Learning Outcomes

This project demonstrates:

Object Detection using YOLO

Convex Hull & Convexity Defects

Real-time AI deployment

Serial communication with microcontrollers

Game loop architecture

Human–AI interaction systems

# 👩‍💻 Author

Irfana Parvin
AI Engineer | Computer Vision Developer
