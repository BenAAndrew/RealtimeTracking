import cv2
import time
import serial
from capture_methods import init_capture_method
from utils import get_arguments, get_dimensions, get_face_position, show_window, send_position_to_arduino


FPS_SAMPLE = 10

# Setup
args = get_arguments()
faceCascade = cv2.CascadeClassifier(args.haarcascade_path)
capture = init_capture_method(args.capture_method)
min_face_size, half_width, half_height = get_dimensions(capture.get_frame(), args.min_face_scale)
if args.arduino_port:
	arduino = serial.Serial(port=args.arduino_port, baudrate=args.arduino_baudrate, timeout=.1)

frames = 0
current_fps = 0
last_sample = time.time()

while True:
    frame = capture.get_frame()
    face = get_face_position(faceCascade, frame, min_face_size, half_width, half_height)

    if args.arduino_port:
        send_position_to_arduino(arduino, face, half_width, half_height)

    if args.preview:
        show_window(
            frame,
            face=face if args.draw_box else None,
            fps=current_fps if args.fps else None,
        )

    # Update FPS
    if frames % FPS_SAMPLE == 0:
        current_fps = int(FPS_SAMPLE / (time.time() - last_sample))
        last_sample = time.time()
    
    frames += 1
    c = cv2.waitKey(1)
    # ESC key
    if c == 27:
        break

# Close capture & cv2 window
capture.close()
cv2.destroyAllWindows()
