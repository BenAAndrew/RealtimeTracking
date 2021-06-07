import cv2
import serial
import time
import json

# Config
with open("config.json") as f:
    config = json.load(f)
arduino_port = config["arduino_port"]
baud_rate = config["baud_rate"]
cascPath = config["haarcascade_path"]
min_face_scale = config["min_face_scale"]
preview = config["preview"]
draw = config["draw"]
show_fps = config["show_fps"]

# Setup
faceCascade = cv2.CascadeClassifier(cascPath)
cap = cv2.VideoCapture(0)
# arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=.1)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Reduces the resolution to improve performance
def get_new_resolution():
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    ratio = height/width

    if ratio == 0.75:
        # 4:3 ratio
        return 320, 240
    elif ratio == 0.5625:
        # 16:9 ratio
        return 640, 360
    else:
        return width, height

# Get dimensions
width, height = get_new_resolution()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
min_face_size = int(min_face_scale * height)
half_width = width // 2
half_height = height // 2
frames = 0
start_time = time.time()

# Sends command to arduino
def handle_position(x, y, w, h):
    centre_x = int(x + w/2)
    centre_y = int(y + h/2)
    x_diff = half_width - centre_x
    y_diff = half_height - centre_y
    message = f"{x_diff},{y_diff}\n"
    print(message[:-1])
    # arduino.write(bytes(message, 'utf-8'))

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(min_face_size, min_face_size)
    )

    if len(faces) > 0:
        # Get coordinates of face closest to centre
        x, y, w, h = sorted(faces, key=lambda x: abs(half_width - x[0]) + abs(half_height - x[1]))[0]
        handle_position(x, y, w, h)

        # Window
        if preview:
            if draw:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if show_fps:
                fps = int(frames/(time.time()-start_time))
                cv2.putText(frame, f"FPS: {fps}", (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow("Face", frame)
    else:
        print("No face detected")

    frames += 1
    c = cv2.waitKey(1)
    if c == 27:
        break

# Close capture & cv2 window
cap.release()
cv2.destroyAllWindows()
