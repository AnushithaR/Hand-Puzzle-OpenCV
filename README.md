#  Hand Gesture Controlled Puzzle Game using OpenCV & MediaPipe

##  Project Overview

The Hand Gesture Controlled Puzzle Game is a real-time Computer Vision application developed using **Python**, **OpenCV**, and **MediaPipe**. The system captures a live image from the webcam using a **two-hand zoom-out gesture**, automatically converts the captured image into a **3×3 sliding puzzle**, shuffles the pieces, and allows users to solve the puzzle using **hand gestures** without touching the keyboard or mouse.

The project demonstrates real-time hand tracking, gesture recognition, image processing, and interactive human-computer interaction.

---

##  Features

-  Real-time webcam capture
-  Automatic photo capture using a two-hand zoom-out gesture
-  Converts the captured image into a 3×3 puzzle
-  Randomly shuffles puzzle pieces
-  Hand gesture-based tile movement using thumb and index finger pinch
-  Real-time timer
-  Move counter
-  Dynamic score calculation
-  Displays "Puzzle Solved!" when completed
-  Attractive user interface with centered puzzle layout
-  Restart game functionality

---

## Technologies Used

- Python 3
- OpenCV
- MediaPipe
- NumPy

---


## Installation

Clone the repository

```bash
git clone https://github.com/YourUsername/Hand-Gesture-Puzzle-Game.git
```

Go to the project folder

```bash
cd Hand-Gesture-Puzzle-Game
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
python gesture_puzzle.py
```

---

## How to Play

### Step 1

Run the application.

The webcam opens automatically.

### Step 2

Position yourself in front of the camera.

### Step 3

Use **both hands** to perform a **zoom-out gesture** by extending both thumbs and index fingers. The application automatically captures your image.

### Step 4

The captured image is divided into a **3×3 puzzle** and shuffled.

### Step 5

Use a **pinch gesture** (thumb and index finger together) to grab a puzzle tile.

### Step 6

Move your hand to another tile position.

### Step 7

Release the pinch gesture to swap the selected tile.

### Step 8

Continue until the puzzle is solved.

---

## Controls

| Action | Gesture |
|---------|---------|
| Capture Image | Two-Hand Zoom-Out Gesture |
| Select Tile | Thumb + Index Finger Pinch |
| Move Tile | Move Hand |
| Drop Tile | Release Pinch |
| Restart | Press **R** |
| Quit | Press **Q** |

---

## Game Information

The application displays:

- Timer
- Move Counter
- Score
- Puzzle Solved Message

---

## Concepts Used

- Computer Vision
- Image Processing
- Hand Tracking
- Gesture Recognition
- Human Computer Interaction (HCI)
- Real-Time Video Processing
- OpenCV
- MediaPipe
- NumPy

---

## Future Enhancements

- Different puzzle sizes (4×4, 5×5)
- Multiple difficulty levels
- Background music and sound effects
- Leaderboard
- High score saving
- Countdown timer mode
- AI-generated puzzles
- Multiplayer mode
- Mobile application version

---

## Author

**Anushitha R**

MCA Graduate | AI & Machine Learning Enthusiast

GitHub: https://github.com/YourUsername

---

## If you like this project

Please consider giving this repository a ⭐ on GitHub.
