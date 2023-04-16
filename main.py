import random
import subprocess

import deeplake
import matplotlib.pyplot as plt
import filters
import datetime
import numpy as np
import os
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier

def debug(msg):
    print(msg, datetime.datetime.now())


if not os.path.exists('yolov3.weights'):
    subprocess.Popen(['wget', 'https://pjreddie.com/media/files/yolov3.weights'])

if not os.path.exists('yolov3.cfg'):
    a = subprocess.check_call(['wget', 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg'])


debug('load')
ds = deeplake.load('hub://activeloop/wiki-art')
i = 0
NUMBER_OF_INSTANCES = 50
debug("randomlist")
rand_list = random.sample(range(0, len(ds.images)), NUMBER_OF_INSTANCES)
colors = {}
x_list = list()
y_list = list()

color_dict = {
    "abstract_expressionism": "#FF5733",
    "action_painting": "#F08080",
    "analytical_cubism": "#7FFFD4",
    "art_nouveau_modern": "#6495ED",
    "baroque": "#8B0000",
    "color_field_painting": "#FFD700",
    "contemporary_realism": "#8FBC8F",
    "cubism": "#FF7F50",
    "early_renaissance": "#FFDAB9",
    "expressionism": "#E9967A",
    "fauvism": "#00FFFF",
    "high_renaissance": "#FFE4C4",
    "impressionism": "#3CB371",
    "mannerism_late_renaissance": "#FFC0CB",
    "minimalism": "#ADD8E6",
    "naive_art_primitivism": "#BDB76B",
    "new_realism": "#FF6347",
    "northern_renaissance": "#DA70D6",
    "pointillism": "#CD5C5C",
    "pop_art": "#00BFFF",
    "post_impressionism": "#8B008B",
    "realism": "#87CEFA",
    "rococo": "#FFA07A",
    "romanticism": "#FF00FF",
    "symbolism": "#228B22",
    "synthetic_cubism": "#FF1493",
    "ukiyo_e": "#800080"
}

for i in rand_list:
    debug('image')
    image = ds.images[i].numpy()
    debug('label')
    label = ds.labels[i].data()
    debug('filter')
    vector = []
    hist = filters.get_histogram(image, False)
    for color in hist:
        vector.append(np.mean(color))
        vector.append(np.std(color))
    vector.append(filters.get_lines_count(image))
    vector.append(filters.get_face_count(image))
    people_cnt, certainty = filters.get_people_count(image)
    vector.append(people_cnt)
    vector.append(filters.get_contour_count(image))

    x_list.append(vector)
    y_list.append(color_dict[label['text'][0]])

clf = RandomForestClassifier(n_estimators=NUMBER_OF_INSTANCES)
clf.fit(x_list, y_list)

# Calculate feature importance scores
importance_scores = clf.feature_importances_
print(importance_scores)
