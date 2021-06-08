import argparse
import cv2


def get_arguments():
    parser = argparse.ArgumentParser(description="Real time face tracking with pan & tilt control")
    parser.add_argument("-m", "--capture_method", type=str, help="Capture method", required=True, choices=["webcam", "raspberrypi"])
    parser.add_argument("-a", "--arduino_port", type=str, help="Port for arduino connection", required=False)
    parser.add_argument("-b", "--arduino_baudrate", type=str, help="Arduino baudrate", required=False)
    parser.add_argument(
        "-c",
        "--haarcascade_path",
        type=str,
        help="Path to Haar cascade classifier file",
        default="haarcascade_frontalface_default.xml",
    )
    parser.add_argument(
        "--min_face_scale", type=float, help="Minimum face size relative to video size (percentage)", default=0.3
    )
    parser.add_argument("--preview", type=bool, help="Whether to show video stream", default=True)
    parser.add_argument("--draw_box", type=bool, help="Whether to draw a box around the face", default=True)
    parser.add_argument("--fps", type=bool, help="Whether to show fps counter", default=False)
    args = parser.parse_args()

    if args.arduino_port and not args.arduino_baudrate:
        raise ValueError("Arduino baudrate not given")
    if args.arduino_baudrate and not args.arduino_port:
        raise ValueError("Arduino port not given")

    return args


def get_dimensions(frame, min_face_scale):
    height, width, _ = frame.shape
    min_face_size = int(min_face_scale * height)
    half_width = width // 2
    half_height = height // 2
    return min_face_size, half_width, half_height


def get_face_position(classifier, frame, min_face_size, half_width, half_height):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(min_face_size, min_face_size))

    if len(faces) > 0:
        # Get coordinates of face closest to centre
        return sorted(faces, key=lambda x: abs(half_width - x[0]) + abs(half_height - x[1]))[0]


def show_window(frame, face=None, fps=None):
    if face is not None:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if fps:
        cv2.putText(frame, f"FPS: {fps}", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow("Face", frame)


def send_position_to_arduino(arduino, face, half_width, half_height):
    x, y, w, h = face
    centre_x = int(x + w / 2)
    centre_y = int(y + h / 2)
    x_diff = half_width - centre_x
    y_diff = half_height - centre_y
    message = f"{x_diff},{y_diff}\n"
    print(message[:-1])
    arduino.write(bytes(message, 'utf-8'))
