"""
file with filters that should return vector
"""

import torch
from torchvision import transforms
import cvlib as cv
import poseEstimate

import cv2
import numpy as np


def get_face_count(img):
    im = img.copy()
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

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
    cv2.imwrite('gr.png',gray)
    gray = cv2.blur(gray, (3, 3))
    cv2.imwrite('blur.png', gray)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    cv2.imwrite('edges.png', edges)
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
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.blur(gray, (7, 7))

    # Perform edge detection
    edges = cv2.Canny(gray, 70, 210)  # Adjust the thresholds as needed

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty image with the same dimensions as the original image
    colored_edges = image.copy()

    # Assign a unique color to each contour/edge
    for i, contour in enumerate(contours):
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        cv2.drawContours(colored_edges, [contour], 0, color, 2)

    return colored_edges, len(contours)


def get_contour_count(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, im = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res_img = img.copy()
    imgd = cv2.drawContours(res_img, contours, -1, (0, 255, 75), 2)
    # see the results
    return imgd, len(contours)


def get_pose_mjeme(image):
    return poseEstimate.run(image_frame=image)

