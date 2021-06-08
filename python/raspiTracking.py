from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils import resize
import time
import cv2

vs = PiVideoStream().start()
frames = 0
time.sleep(2)
display = True
show_fps = True
start_time = time.time()

while True:
	frame = vs.read()
	frame = resize(frame, width=400)

	if display:
		if show_fps:
			fps = int(frames/(time.time()-start_time))
			cv2.putText(frame, f"FPS: {fps}", (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
		cv2.imshow("Face", frame)
		
	frames += 1
	
	c = cv2.waitKey(1)
	# ESC key
	if c == 27:
		break

cv2.destroyAllWindows()
vs.stop()
