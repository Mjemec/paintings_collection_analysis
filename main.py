import random
import subprocess

import json
import cv2
import deeplake
import matplotlib.pyplot as plt
import filters
import datetime
import numpy as np
import os
import shutil
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier
from website import img_dir, tag_dir


def debug(msg):
    print(msg, datetime.datetime.now())


if not os.path.exists('yolov3.weights'):
    subprocess.Popen(['wget', 'https://pjreddie.com/media/files/yolov3.weights'])

if not os.path.exists('yolov3.cfg'):
    a = subprocess.check_call(['wget', 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg'])

# i = 0
NUMBER_OF_INSTANCES = 10


x_list = list()
y_list = list()

times = ["early_renaissance", "high_renaissance", "mannerism_late_renaissance", "northern_renaissance", "baroque",
         "ukiyo_e", "rococo", "realism", "impressionism", "romanticism", "symbolism", "pointillism",
         "art_nouveau_modern", "naive_art_primitivism", "post_impressionism", "fauvism", "cubism", "analytical_cubism",
         "expressionism", "synthetic_cubism", "color_field_painting",
         "abstract_expressionism", "action_painting", "pop_art", "contemporary_realism", "new_realism", "minimalism"]

colors_by_time = ['#FFDAB9', '#FFE4C4', '#FFC0CB', '#DA70D6', '#8B0000', '#800080', '#FFA07A', '#87CEFA', '#3CB371',
                  '#FF00FF', '#228B22', '#CD5C5C', '#6495ED', '#8B008B', '#00FFFF', '#FF7F50', '#7FFFD4', '#E9967A',
                  '#FF1493', '#FF1493', '#E9967A', '#FFD700', '#FF5733', '#F08080', '#00BFFF', '#8FBC8F', '#FF6347',
                  '#ADD8E6', "#BDB76B"]

# clear directory with images
if os.path.isdir(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

# clear directory with tags
if os.path.isdir(tag_dir):
    shutil.rmtree(tag_dir)
os.mkdir(tag_dir)

by_group_all = dict()
for time in times:
    by_group_all[time] = []


def do_image(image, time_period, img_dir, i):
    vector = []
    img_tag = {}
    hist = filters.get_histogram(image, False)

    poses, cnt = filters.get_pose_mjeme(image)
    cv2.imwrite(img_dir + "/image_" + str(i) + "_pose.jpg", poses)
    if not handpicked:
        cv2.imwrite(img_dir + "/image_" + str(i) + ".jpg", image)

    # histogram
    for j in range(len(hist)):
        color = hist[j]
        mean = (color * np.array(range(0, 256))).sum() / color.sum()
        std = np.std(color)
        vector.append(mean)
        vector.append(std)
        img_tag["color_" + str(j) + "_mean"] = mean
        img_tag["color_" + str(j) + "_std"] = std
    print("")

    # line count
    lines_image, line_count = filters.get_lines_count(image)
    cv2.imwrite(img_dir + "/image_" + str(i) + "_lines.jpg", lines_image)
    vector.append(line_count)
    img_tag["line_count"] = line_count

    # face count
    face_image, face_count = filters.get_face_count(image)
    cv2.imwrite(img_dir + "/image_" + str(i) + "_faces.jpg", face_image)
    vector.append(face_count)
    img_tag["face_count"] = face_count

    # people count
    vector.append(cnt)
    img_tag["people_count"] = cnt

    # contour count
    cont_img, contour_count = filters.get_contour_count(image)
    cv2.imwrite(img_dir + "/image_" + str(i) + "_contour.jpg", cont_img)
    vector.append(contour_count)
    img_tag["contour_count"] = contour_count

    x_list.append(vector)
    y_list.append(time_period)
    img_tag["time_period"] = time_period

    # serializing json
    tag_json = json.dumps(img_tag, indent=4)

    # write image tag in json format
    with open(tag_dir + "/image_" + str(i) + ".json", "w") as tag_file:
        tag_file.write(tag_json)
    global by_group_all
    by_group_all[time_period].append(vector)


handpicked = True
if handpicked:
    for time_period in os.listdir('imgCollection'):
        debug(time_period)
        if time_period.endswith('.sh'):
            continue
        for picture in os.listdir(os.path.join('imgCollection', time_period)):
            if len(os.path.splitext(picture)[0].split('_')) == 2:
                i = os.path.splitext(picture)[0].split('_')[1]
                image = cv2.imread(os.path.join('imgCollection', time_period, picture))
                im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img_path = os.path.join('imgCollection', time_period)
                do_image(image, time_period, img_path, i)
else:
    ds = deeplake.load('hub://activeloop/wiki-art')
    rand_list = random.sample(range(0, len(ds.images)), NUMBER_OF_INSTANCES)
    for i in rand_list:
        debug('image #' + str(i))
        image = ds.images[i].numpy()
        im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        debug('label')
        label = ds.labels[i].data()
        time_period = label['text'][0]
        debug('filter')
        do_image(im_rgb, time_period, img_dir, i)

do_json = False
if do_json:
    with open('by_group_all.json', 'w+') as f:
        data = json.dumps(by_group_all)
        f.write(data)

    by_group_new = dict()
    for e in times:
        tmp = by_group_all[e]
        h = np.array(tmp)
        if len(tmp):
            by_group_new[e] = list(h.mean(axis=0))

    with open('by_group.json', 'w+') as f:
        data = json.dumps([times, by_group_new], indent=4)
        f.write(data)





