import cv2
import mediapipe as mp
import pyautogui
import time
import threading
import queue
import math
from cursor_functions import right_click, left_click

# Camera setup
cam = cv2.VideoCapture(0)
cam.set(3,1280) # width
cam.set(4,720) # height

# MediaPipe hand detection setup
mpHands = mp.solutions.hands
handDetector = mpHands.Hands(max_num_hands=1, min_detection_confidence = 0.8, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# screen dimensions for cursor mapping
screen_w, screen_h = pyautogui.size()

# FPS calculation variables
ptime = 0 # previous time
ctime = 0 # current time

cursor_queue = queue.Queue(maxsize=1)

# Background worker thread for smooth cursor movement
def cursor_worker():
    while True:
        x, y = cursor_queue.get()
        pyautogui.moveTo(x, y)

threading.Thread(target=cursor_worker, daemon=True).start()

# Helper function to calculate distance between two points
def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

# tracks whether gestures is currently active
left_mouse_click = False
right_mouse_click = False
drag_movement = False

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

            thumb_tip_px = [int(thumb_tip.x * w), int(thumb_tip.y * h)]
            index_finger_tip_px = [int(index_finger_tip.x * w), int(index_finger_tip.y * h)]
            middle_finger_tip_px = [int(middle_finger_tip.x * w), int(middle_finger_tip.y * h)]
            ring_finger_tip_px = [int(ring_finger_tip.x * w), int(ring_finger_tip.y * h)]

            # Move Cursor (using index finger)
            margin = 5
            mouse_x = max(margin, min(int(index_finger_tip.x * screen_w), screen_w - margin))
            mouse_y = max(margin, min(int(index_finger_tip.y * screen_h), screen_h - margin))

            try:
                cursor_queue.put_nowait((mouse_x, mouse_y))
            except queue.Full:
                pass

            # Hold and Move
            hm_distance = euclidean_distance(ring_finger_tip_px, middle_finger_tip_px)
            print(hm_distance)
            if hm_distance < 30:
                if not drag_movement:
                    pyautogui.mouseDown()
                    drag_movement = True

                pyautogui.moveTo(mouse_x, mouse_y)

            elif hm_distance > 30:
                if drag_movement:
                    pyautogui.mouseUp()
                    drag_movement = False

            if not drag_movement:
                # Left Click
                lc_distance = euclidean_distance(thumb_tip_px, middle_finger_tip_px)
                if lc_distance < 30:
                    if not left_mouse_click:
                        left_click(mouse_x, mouse_y)
                        left_mouse_click = True
                else:
                    left_mouse_click = False

                # Right Click
                rc_distance = euclidean_distance(thumb_tip_px, ring_finger_tip_px)
                if rc_distance < 30:
                    if not right_mouse_click:
                        right_click(mouse_x, mouse_y)
                        right_mouse_click = True
                else:
                    right_mouse_click = False

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()