"""
file with filters that should return vector
"""

import torch
from torchvision import transforms

import poseEstimate

import cv2
import numpy as np
from ultralyticsplus import YOLO, render_result

from matplotlib import pyplot as plt

def get_face_count(image):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    return None, len(faces)


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
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 100
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 100  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    return lines_edges, len(lines)


def get_contour_count(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return len(contours)


def get_pose_mjeme(image):
    return poseEstimate.run(image_frame=image)

