import cv2
import numpy as np
import mediapipe as mp

cam = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
handDetector = mpHands.Hands(max_num_hands=2, min_detection_confidence = 0.8, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame,1) #Inverts Camera
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, x = rgb_frame.shape

    output = handDetector.process(rgb_frame)
    landmarkList = output.multi_hand_landmarks

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


    cv2.imshow('Frame', frame)
    cv2.waitKey(1)