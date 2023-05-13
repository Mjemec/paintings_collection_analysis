"""
file with filters that should return vector
"""

import torch
from torchvision import transforms

import poseEstimate

import cv2
import numpy as np


def get_face_count(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    faces, confidences = cv.detect_face(im, 0.2)
    # loop through detected faces and add bounding box
    for face in faces:
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]
        # draw rectangle over face
        cv2.rectangle(im, (startX, startY), (endX, endY), (0, 255, 0), 2)
    return im, len(faces)


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


def detect_lines(image, threshold, min_line_length, max_line_gap):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)

    if lines is None:
        return []

    detected_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        score = calculate_line_score(line, edges)
        detected_lines.append((x1, y1, x2, y2, score))

    return detected_lines


def calculate_line_score(line, edges):
    x1, y1, x2, y2 = line[0]
    line_segment = edges[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
    line_length = np.sum(line_segment) / 255
    return line_length / np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def non_max_suppression(lines, threshold, count=20):
    if len(lines) == 0:
        return []

    lines = np.array(lines)
    x1 = lines[:, 0]
    y1 = lines[:, 1]
    x2 = lines[:, 2]
    y2 = lines[:, 3]
    scores = lines[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(scores)

    keep = []
    while len(order) > 0:
        count -= 1
        last = len(order) - 1
        i = order[last]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[:last]])
        yy1 = np.maximum(y1[i], y1[order[:last]])
        xx2 = np.minimum(x2[i], x2[order[:last]])
        yy2 = np.minimum(y2[i], y2[order[:last]])

        width = np.maximum(0, xx2 - xx1 + 1)
        height = np.maximum(0, yy2 - yy1 + 1)
        intersection = width * height

        overlap = intersection / (areas[i] + areas[order[:last]] - intersection)

        inds = np.where(overlap <= threshold)[0]
        order = order[inds]
        if count <= 0:
            return lines[keep]
    return lines[keep]


def get_lines_count(img):
    image = img.copy()

    threshold = 100  # Minimum number of intersections to detect a line
    min_line_length = 50  # Minimum length of the line to be detected
    max_line_gap = 10  # Maximum allowed gap between line segments to be considered as a single line
    nms_threshold = 0.5  # Overlap threshold for non-maximum suppression

    detected_lines = detect_lines(image, threshold, min_line_length, max_line_gap)
    filtered_lines = non_max_suppression(detected_lines, nms_threshold)

    for line in filtered_lines:
        x1, y1, x2, y2, score = line
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, f"Score: {score:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, len(filtered_lines)


def get_contour_count(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return len(contours)


def get_pose_mjeme(image):
    return poseEstimate.run(image_frame=image)

