import cv2
import numpy as np
import serial
from ultralytics import YOLO
import time

# =========================
# INITIAL SETUP
# =========================

model = YOLO("hand_yolov8n.pt")

arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)

last_gesture = ""
ai_gesture = "WAIT"

user_score = 0
system_score = 0

GAME_DURATION = 60  # seconds
start_time = time.time()
game_over = False

# =========================
# GESTURE CLASSIFICATION
# =========================

def classify_gesture(hand_img):
    gray = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return "UNKNOWN"

    hand = max(contours, key=cv2.contourArea)
    if cv2.contourArea(hand) < 3000:
        return "UNKNOWN"

    hull = cv2.convexHull(hand, returnPoints=False)
    if hull is None or len(hull) < 3:
        return "ROCK"

    defects = cv2.convexityDefects(hand, hull)
    if defects is None:
        return "ROCK"

    finger_count = 0
    for i in range(defects.shape[0]):
        _, _, _, d = defects[i, 0]
        if d > 10000:
            finger_count += 1

    if finger_count == 0:
        return "ROCK"
    elif finger_count == 1:
        return "SCISSORS"
    else:
        return "PAPER"

# =========================
# AI LOGIC
# =========================

def system_choice(user):
    return {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}.get(user, "UNKNOWN")

def decide_winner(user, system):
    if user == system:
        return "DRAW"
    elif (user == "ROCK" and system == "SCISSORS") or \
         (user == "PAPER" and system == "ROCK") or \
         (user == "SCISSORS" and system == "PAPER"):
        return "USER"
    else:
        return "SYSTEM"

# =========================
# MAIN LOOP
# =========================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, GAME_DURATION - elapsed_time)

    if remaining_time == 0:
        game_over = True

    results = model(frame, conf=0.5)

    if not game_over:
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                hand_img = frame[y1:y2, x1:x2]

                if hand_img.size == 0:
                    continue

                gesture = classify_gesture(hand_img)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"USER: {gesture}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if gesture != last_gesture and gesture != "UNKNOWN":
                    ai_gesture = system_choice(gesture)
                    result = decide_winner(gesture, ai_gesture)

                    if result == "USER":
                        user_score += 1
                    elif result == "SYSTEM":
                        system_score += 1

                    arduino.write((ai_gesture + "\n").encode())
                    last_gesture = gesture

                cv2.putText(frame, f"AI: {ai_gesture}",
                            (x1, y2 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # =========================
    # UI OVERLAY
    # =========================

    cv2.rectangle(frame, (10, 10), (380, 150), (0, 0, 0), -1)

    cv2.putText(frame, f"TIME: {remaining_time}s",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    cv2.putText(frame, f"USER: {user_score}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"SYSTEM: {system_score}",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if game_over:
        winner = "DRAW"
        if user_score > system_score:
            winner = "USER WINS 🎉"
        elif system_score > user_score:
            winner = "SYSTEM WINS 🤖"

        cv2.putText(frame, "GAME OVER",
                    (420, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        cv2.putText(frame, winner,
                    (420, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    cv2.putText(frame, "Press R to Restart | ESC to Quit",
                (420, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Rock Paper Scissors - Timed Match", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('r'):
        user_score = 0
        system_score = 0
        last_gesture = ""
        ai_gesture = "WAIT"
        start_time = time.time()
        game_over = False

# =========================
# CLEANUP
# =========================

cap.release()
cv2.destroyAllWindows()
arduino.close()
