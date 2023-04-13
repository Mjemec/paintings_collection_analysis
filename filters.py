"""
file with filters that should return vector
"""
import cv2
import numpy as np


def get_histogram(image, flat=True):
    hist_1 = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_2 = cv2.calcHist([image], [1], None, [256], [0, 256])
    hist_3 = cv2.calcHist([image], [2], None, [256], [0, 256])

    hists = list()
    hists.append(np.array((hist_1/np.sum(hist_1)).T.tolist()[0]))
    hists.append(np.array((hist_2/np.sum(hist_2)).T.tolist()[0]))
    hists.append(np.array((hist_3/np.sum(hist_3)).T.tolist()[0]))
    if flat:
        return np.array(hists).flatten()
    else:
        return np.array(hists)
