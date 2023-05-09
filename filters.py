"""
file with filters that should return vector
"""

import torch
from torchvision import transforms

import poseEstimate

import cv2
import numpy as np

from matplotlib import pyplot as plt

def get_face_count(image):
    return poseEstimate.run(poseweights='yolov8n-face.pt', image_frame=image)


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


def get_pose_mjeme(image):
    return poseEstimate.run(image_frame=image)

