"""
file with filters that should return vector
"""
import cv2
import numpy as np
import os

def get_face_count(img):
	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
	return len(faces)

def get_people_count(img):
	# Load pre-trained YOLOv3 model for object detection
	net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

	# Get names of output layers
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

	# Load image and convert to blob format
	img_blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255, size=(416, 416), swapRB=True, crop=False)

	# Set input for YOLOv3 network
	net.setInput(img_blob)

	# Run forward pass through YOLOv3 network
	detections = net.forward(output_layers)

	# Initialize counters for people and confidence scores
	num_people = 0
	confidences = []

	# Loop over detected objects and count people
	for detection in detections:
		for detected_object in detection:
			scores = detected_object[5:]
			class_id = np.argmax(scores)

			if class_id == 0:  # Class ID 0 is for people
				confidence = scores[class_id]
				if confidence > 0.5:  # Set threshold for confidence score
					num_people += 1
					confidences.append(float(confidence))

	# Return number of people and average confidence score
	return num_people, np.mean(confidences)


def get_histogram(image, flat=True):
	hist_1 = cv2.calcHist([image], [0], None, [256], [0, 256])
	hist_2 = cv2.calcHist([image], [1], None, [256], [0, 256])
	hist_3 = cv2.calcHist([image], [2], None, [256], [0, 256])

	hists = list()
	hists.append(np.array(hist_1.T.tolist()[0]))
	hists.append(np.array(hist_2.T.tolist()[0]))
	hists.append(np.array(hist_3.T.tolist()[0]))
	if flat:
		return np.array(hists).flatten()
	else:
		return np.array(hists)


def get_lines_count(img):
	# Convert image to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Apply edge detection
	edges = cv2.Canny(gray, 50, 150, apertureSize=3)

	# Apply Hough transform to detect lines
	lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

	# Count number of lines
	num_lines = 0
	if lines is not None:
		num_lines = len(lines)

	return num_lines


def get_contour_count(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Threshold the image
	thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

	# Find contours in the thresholded image
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	return len(contours)
