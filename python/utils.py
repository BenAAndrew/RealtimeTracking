import cv2


def get_face_position(classifier, frame, min_face_size=50, half_width=160, half_height=240):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(min_face_size, min_face_size)
    )

    if len(faces) > 0:
        # Get coordinates of face closest to centre
        return sorted(faces, key=lambda x: abs(half_width - x[0]) + abs(half_height - x[1]))[0]


def show_window(frame, face=None, fps=None):
    if face:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if fps:
        cv2.putText(frame, f"FPS: {fps}", (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow("Face", frame)
