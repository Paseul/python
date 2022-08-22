import cv2
import numpy as np

# extract the model name and model scale from the file path
path = "models/ESPCN_x4.pb"
modelScale = 4

sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(path)
sr.setModel("espcn", 4) # set the model by passing the value and the upsampling ratio

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
cap = cv2.VideoCapture("videos/run.mp4")
outputFile = 'videos/run_sr_out_py.avi'

# Get the video writer initialized to save the output video
vid_writer = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)*modelScale),round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*modelScale)))

# loop over the frames from the video stream
while cv2.waitKey(1) < 0:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 300 pixels
	hasFrame, frame = cap.read()

	# upscale the frame using the super resolution model and then
	# bicubic interpolation (so we can visually compare the two)
	upscaled = sr.upsample(frame)

	# Write the frame with the detection boxes
	vid_writer.write(upscaled.astype(np.uint8))

	# show the original frame, bicubic interpolation frame, and super
	# resolution frame
	cv2.imshow("Original", frame)
	cv2.imshow("Super Resolution", upscaled)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
cap.stop()