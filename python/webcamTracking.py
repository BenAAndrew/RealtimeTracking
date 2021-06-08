import cv2
import time
from utils import get_arguments, get_dimensions, get_face_position, show_window

# Get webcam feed
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Setup
args = get_arguments()
faceCascade = cv2.CascadeClassifier(args.haarcascade_path)
ret, frame = cap.read()
min_face_size, half_width, half_height = get_dimensions(frame, args.min_face_scale)
frames = 0
start_time = time.time()

while True:
    _, frame = cap.read()
    face = get_face_position(faceCascade, frame, min_face_size, half_width, half_height)

    if args.preview:
        show_window(
            frame,
            face=face if args.draw_box else None,
            fps=int(frames / (time.time() - start_time)) if args.fps else None,
        )

    frames += 1
    c = cv2.waitKey(1)
    # ESC key
    if c == 27:
        break

# Close capture & cv2 window
cap.release()
cv2.destroyAllWindows()
