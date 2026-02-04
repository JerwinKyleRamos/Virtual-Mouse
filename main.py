import cv2
import mediapipe as mp
import pyautogui
import time
import threading
from cursor_functions import move_cursor

cam = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
handDetector = mpHands.Hands(max_num_hands=1, min_detection_confidence = 0.8, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

ptime = 0
ctime = 0

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame,1) #Inverts Camera
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = rgb_frame.shape

    # Calculate and Displays Frame FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(frame,f'FPS: {int(fps)}', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    output = handDetector.process(rgb_frame)
    landmarkList = output.multi_hand_landmarks

    # Creates a Bounding Box
    if landmarkList:
        for handLandmark in landmarkList:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLandmark.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y
                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            mp_drawing.draw_landmarks(frame, handLandmark, mpHands.HAND_CONNECTIONS)

            thumb_tip = handLandmark.landmark[4]
            index_finger_tip = handLandmark.landmark[8]
            middle_finger_tip = handLandmark.landmark[12]
            ring_finger_tip = handLandmark.landmark[16]
            pinky_finger_tip = handLandmark.landmark[20]

            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            middle_finger_tip_x, middle_finger_tip_y = int(middle_finger_tip.x * w), int(middle_finger_tip.y * h)
            # ring_finger_tip_x, ring_finger_tip_y = int(ring_finger_tip.x * w), int(ring_finger_tip.y * h)
            # pinky_finger_tip_x, pinky_finger_tip_y = int(pinky_finger_tip.x * w), int(pinky_finger_tip.y * h)

            #To do: Mouse Functionalities to Create (move, rightclick, leftclick, Doubleclick, drag, scroll)

            # Move Cursor (using index)
            margin = 10
            mouse_x = max(margin, min(int(index_finger_tip.x * screen_w), screen_w - margin))
            mouse_y = max(margin, min(int(index_finger_tip.y * screen_h), screen_h - margin))
            threading.Thread(target=move_cursor, args=(mouse_x, mouse_y), daemon=True).start()



    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()