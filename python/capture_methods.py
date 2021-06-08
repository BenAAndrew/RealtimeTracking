from abc import ABC, abstractmethod
import cv2
import time


class CaptureMethod(ABC):
    @abstractmethod
    def get_frame(self):
        pass

    @abstractmethod
    def close(self):
        pass


class Webcam(CaptureMethod):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def get_frame(self):
        _, frame = self.cap.read()
        return frame

    def close(self):
        self.cap.release()


class RaspberryPi(CaptureMethod):
    def __init__(self):
        from imutils.video.pivideostream import PiVideoStream
        self.vs = PiVideoStream().start()
        time.sleep(2)

    def get_frame(self):
        return self.vs.read()

    def close(self):
        self.vs.stop()


def init_capture_method(capture_method):
    if capture_method == "webcam":
        return Webcam()
    elif capture_method == "raspberrypi":
        return RaspberryPi()
    else:
        raise AttributeError("Invalid capture method. Must be on of: "+(', ').join(["webcam", "raspberrypi"]))
