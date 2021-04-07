# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

init = 0

fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the video stream, resize it, and convert it
	frame = vs.read()	

	# show the output frame
	cv2.imshow("Frame", frame)

	if init == 0:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter("output.mp4", fourcc, 275,
			(frame.shape[1], frame.shape[0]), True)
		init = 1

	fps.update()
	fps.stop()
	text = "{:.2f}".format(fps.fps())
	cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

	writer.write(frame)	

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
writer.release()
vs.stop()