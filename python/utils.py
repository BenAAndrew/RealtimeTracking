import cv2


def get_face_position(classifier, frame, min_face_size, max_face_size, half_width, half_height):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(min_face_size, max_face_size)
    )

    if len(faces) > 0:
        # Get coordinates of face closest to centre
        return sorted(faces, key=lambda x: abs(half_width - x[0]) + abs(half_height - x[1]))[0]
