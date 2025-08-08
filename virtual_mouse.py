import cv2
import mediapipe as mp
import pyautogui
import time

# Webcam
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

dragging = False

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            landmarks = hand_landmark.landmark

            # Coordinates
            index_x = int(landmarks[8].x * w)
            index_y = int(landmarks[8].y * h)
            thumb_x = int(landmarks[4].x * w)
            thumb_y = int(landmarks[4].y * h)
            middle_x = int(landmarks[12].x * w)
            middle_y = int(landmarks[12].y * h)

            # Move Mouse
            screen_x = screen_w / w * index_x
            screen_y = screen_h / h * index_y
            pyautogui.moveTo(screen_x, screen_y)

            # Distances
            dist_thumb_index = ((thumb_x - index_x)**2 + (thumb_y - index_y)**2)**0.5
            dist_thumb_middle = ((thumb_x - middle_x)**2 + (thumb_y - middle_y)**2)**0.5

            # ---- Drag and Drop ----
            if dist_thumb_index < 30:
                if not dragging:
                    dragging = True
                    pyautogui.mouseDown()
                    print("Drag Start")
            else:
                if dragging:
                    dragging = False
                    pyautogui.mouseUp()
                    print("Drop")

            # ---- Right Click ----
            if dist_thumb_middle < 30:
                pyautogui.rightClick()
                time.sleep(0.3)

            # ---- Scroll ----
            # Get finger directions
            index_tip = landmarks[8]
            index_pip = landmarks[6]
            middle_tip = landmarks[12]
            middle_pip = landmarks[10]

            index_dir = index_tip.y - index_pip.y
            middle_dir = middle_tip.y - middle_pip.y

            # If both fingers are up
            if index_dir < -0.03 and middle_dir < -0.03:
                pyautogui.scroll(20)  # Scroll Up
                print("Scroll Up")
                time.sleep(0.2)
            elif index_dir > 0.03 and middle_dir > 0.03:
                pyautogui.scroll(-20)  # Scroll Down
                print("Scroll Down")
                time.sleep(0.2)

            draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Display
    cv2.imshow("Virtual Mouse with Scroll & Drag", frame)

    if cv2.waitKey(1) == ord('q'):
        break
