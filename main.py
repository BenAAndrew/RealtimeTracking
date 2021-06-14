import cv2
import time
from capture_methods import init_capture_method
from utils import get_arguments, get_dimensions, get_face_position, show_window


FPS_SAMPLE = 10

# Setup
args = get_arguments()
faceCascade = cv2.CascadeClassifier(args.haarcascade_path)
capture = init_capture_method(args.capture_method)
min_face_size, half_width, half_height = get_dimensions(capture.get_frame(), args.min_face_scale)

if args.motor_control:
    from motor_control import send_position_to_motors, PAN_MOTOR_PIN, TILT_MOTOR_PIN
    import pigpio
    pi = pigpio.pi()

frames = 0
current_fps = 0
last_sample = time.time()

try:
    while True:
        frame = capture.get_frame()
        face = get_face_position(faceCascade, frame, min_face_size, half_width, half_height)

        if args.motor_control and face is not None:
            send_position_to_motors(face, half_width, half_height)

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
finally:
    # Close capture & cv2 window
    capture.close()
    cv2.destroyAllWindows()

    if args.motor_control:
        pi.set_servo_pulsewidth(PAN_MOTOR_PIN, 0)
        pi.stop()
