# Virtual Mouse using Hand Gestures

## Overview

Virtual-Mouse is a computer vision–based project that simulates mouse functionality using hand and finger movements. Instead of a physical mouse, the system tracks your fingers through a webcam and translates specific gestures into mouse actions such as moving the cursor, left click, right click, click-and-hold, and drag.

This project demonstrates how hand-tracking technology can be used to create touch-free human–computer interaction.

## Features

  - Cursor movement using finger tracking

  - Left click

  - Right click

  - Click and hold

  - Drag and move

  - Real-time hand detection via webcam

## How It Works

The system uses MediaPipe to detect and track hand landmarks in real time. Based on the position and movement of specific fingers, different mouse actions are triggered.
PyAutoGUI is used to control the system mouse, while OpenCV handles video capture and image processing.

## Libraries Used

MediaPipe – for hand and finger landmark detection

OpenCV (cv2) – for webcam access and image processing

PyAutoGUI – for controlling mouse movements and clicks
