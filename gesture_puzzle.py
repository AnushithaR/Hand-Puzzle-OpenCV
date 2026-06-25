import cv2
import mediapipe as mp
import numpy as np
import random
import math
import time

GRID = 3
CAM_WIDTH, CAM_HEIGHT = 900, 650
PUZZLE_SIZE = 450

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

captured = False
capture_time = 0
tiles = []
positions = []

selected_tile = None
dragging = False

moves = 0
start_time = None
solved = False


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def split_image(img):
    img = cv2.resize(img, (PUZZLE_SIZE, PUZZLE_SIZE))
    tile_size = PUZZLE_SIZE // GRID
    result = []

    for r in range(GRID):
        for c in range(GRID):
            tile = img[r*tile_size:(r+1)*tile_size,
                       c*tile_size:(c+1)*tile_size]
            result.append(tile)

    return result


def shuffle_positions():
    pos = list(range(GRID * GRID))
    while True:
        random.shuffle(pos)
        if pos != list(range(GRID * GRID)):
            return pos


def check_solved(positions):
    return positions == list(range(GRID * GRID))


def draw_background(frame):
    bg = np.zeros_like(frame)
    bg[:] = (20, 20, 35)

    cv2.putText(bg, "HAND GESTURE PUZZLE", (250, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    return bg


def draw_puzzle(bg, tiles, positions, selected_tile=None):
    start_x = (CAM_WIDTH - PUZZLE_SIZE) // 2
    start_y = 130
    tile_size = PUZZLE_SIZE // GRID

    cv2.rectangle(bg, (start_x - 15, start_y - 15),
                  (start_x + PUZZLE_SIZE + 15, start_y + PUZZLE_SIZE + 15),
                  (80, 80, 120), -1)

    for i, tile_index in enumerate(positions):
        r = i // GRID
        c = i % GRID

        x = start_x + c * tile_size
        y = start_y + r * tile_size

        bg[y:y+tile_size, x:x+tile_size] = tiles[tile_index]

        color = (0, 255, 0) if selected_tile == i else (255, 255, 255)

        cv2.rectangle(bg, (x, y), (x + tile_size, y + tile_size),
                      color, 3)

    return bg


def get_tile_from_finger(x, y):
    start_x = (CAM_WIDTH - PUZZLE_SIZE) // 2
    start_y = 130
    tile_size = PUZZLE_SIZE // GRID

    if start_x <= x <= start_x + PUZZLE_SIZE and start_y <= y <= start_y + PUZZLE_SIZE:
        col = (x - start_x) // tile_size
        row = (y - start_y) // tile_size
        return int(row * GRID + col)

    return None


with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
) as hands:

    while True:
        success, frame = cap.read()

        if not success:
            print("Camera not opening")
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        display = draw_background(frame)

        if not captured:
            display[120:480, 270:630] = cv2.resize(frame, (360, 360))

            cv2.rectangle(display, (270, 120), (630, 480),
                          (255, 255, 255), 4)

            cv2.putText(display, "Show both hands zoom-out to capture",
                        (210, 540), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)

            if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
                hand_points = []

                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(display, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    h, w, _ = frame.shape

                    thumb = hand_landmarks.landmark[4]
                    index = hand_landmarks.landmark[8]

                    thumb_point = (int(thumb.x * w), int(thumb.y * h))
                    index_point = (int(index.x * w), int(index.y * h))

                    hand_points.append((thumb_point, index_point))

                    cv2.circle(display, thumb_point, 12, (0, 255, 0), -1)
                    cv2.circle(display, index_point, 12, (0, 255, 0), -1)

                left_thumb, left_index = hand_points[0]
                right_thumb, right_index = hand_points[1]

                d1 = distance(left_thumb, right_thumb)
                d2 = distance(left_index, right_index)

                if d1 > 230 and d2 > 230:
                    cv2.putText(display, "Capturing...",
                                (360, 600), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 3)

                    if time.time() - capture_time > 1:
                        photo = frame.copy()
                        tiles = split_image(photo)
                        positions = shuffle_positions()

                        captured = True
                        start_time = time.time()
                        moves = 0
                        solved = False
                        selected_tile = None
                        dragging = False
                else:
                    capture_time = time.time()

        else:
            display = draw_puzzle(display, tiles, positions, selected_tile)

            elapsed_time = int(time.time() - start_time)
            score = max(1000 - moves * 10 - elapsed_time, 0)

            cv2.putText(display, f"Moves: {moves}", (40, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.putText(display, f"Score: {score}", (360, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.putText(display, f"Time: {elapsed_time}s", (700, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.putText(display, "Pinch to grab | Move hand | Open fingers to drop",
                        (130, 610), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 255), 2)

            if solved:
                cv2.rectangle(display, (210, 260), (690, 380),
                              (0, 0, 0), -1)

                cv2.putText(display, "PUZZLE SOLVED!",
                            (250, 330), cv2.FONT_HERSHEY_SIMPLEX,
                            1.3, (0, 255, 0), 4)

            if result.multi_hand_landmarks and not solved:
                hand_landmarks = result.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(display, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w, _ = display.shape

                thumb = hand_landmarks.landmark[4]
                index = hand_landmarks.landmark[8]

                thumb_point = (int(thumb.x * w), int(thumb.y * h))
                index_point = (int(index.x * w), int(index.y * h))

                finger_x, finger_y = index_point

                pinch_distance = distance(thumb_point, index_point)
                current_tile = get_tile_from_finger(finger_x, finger_y)

                cv2.circle(display, index_point, 15, (0, 255, 0), -1)
                cv2.line(display, thumb_point, index_point, (0, 255, 255), 3)

                if pinch_distance < 45 and not dragging:
                    if current_tile is not None:
                        selected_tile = current_tile
                        dragging = True
                        print("Grabbed tile:", selected_tile + 1)

                elif pinch_distance >= 65 and dragging:
                    drop_tile = current_tile

                    if drop_tile is not None and selected_tile is not None:
                        if drop_tile != selected_tile:
                            positions[selected_tile], positions[drop_tile] = (
                                positions[drop_tile],
                                positions[selected_tile]
                            )

                            moves += 1

                            if check_solved(positions):
                                solved = True

                            print("Dropped and swapped")

                    selected_tile = None
                    dragging = False

        cv2.imshow("Hand Gesture Puzzle Game", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            captured = False
            selected_tile = None
            dragging = False
            moves = 0
            start_time = None
            solved = False

        elif key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()