from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import time
import cv2
from utils import get_face_position, show_window

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
vs = PiVideoStream().start()
frames = 0
time.sleep(2)
display = True
show_fps = True
start_time = time.time()

while True:
	frame = vs.read()
	face = get_face_position(faceCascade, frame)

	if display:
		show_window(frame, face, fps=int(frames/(time.time()-start_time)) if show_fps else None)
		
	frames += 1
	c = cv2.waitKey(1)
	# ESC key
	if c == 27:
		break

cv2.destroyAllWindows()
vs.stop()
