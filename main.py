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

debug('load')
ds = deeplake.load('hub://activeloop/wiki-art')
i = 0
NUMBER_OF_INSTANCES = 20
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

# clear directory with images
if os.path.isdir(img_dir):
	shutil.rmtree(img_dir)
os.mkdir(img_dir)

# clear directory with tags
if os.path.isdir(tag_dir):
	shutil.rmtree(tag_dir)
os.mkdir(tag_dir)

for i in rand_list:
	debug('image #' + str(i))
	image = ds.images[i].numpy()
	debug('write image to file')
	cv2.imwrite(img_dir + "/image_" + str(i) + ".jpg", image)

	debug('label')
	label = ds.labels[i].data()

	debug('filter')
	vector = []
	img_tag = {}
	hist = filters.get_histogram(image, False)

	# histogram
	for j in range(len(hist)):
		color = hist[j]
		mean = (color*np.array(range(0, 256))).sum()/color.sum()
		std = np.std(color)
		vector.append(mean)
		vector.append(std)
		img_tag["color_" + str(j) + "_mean"] = mean
		img_tag["color_" + str(j) + "_std"] = std
	print("")

	# line count
	line_count = filters.get_lines_count(image)
	vector.append(line_count)
	img_tag["line_count"] = line_count

	# face count
	face_count = filters.get_face_count(image)
	vector.append(face_count)
	img_tag["face_count"] = face_count

	# people count
	people_count, certainty = filters.get_people_count(image)
	vector.append(people_count)
	img_tag["people_count"] = people_count

	# contour count
	contour_count = filters.get_contour_count(image)
	vector.append(contour_count)
	img_tag["contour_count"] = contour_count

	x_list.append(vector)
	y_list.append(color_dict[label['text'][0]])

	# serializing json
	tag_json = json.dumps(img_tag, indent=4)

	# write image tag in json format
	with open(tag_dir + "/image_" + str(i) + ".json", "w") as tag_file:
		tag_file.write(tag_json)

clf = RandomForestClassifier(n_estimators=NUMBER_OF_INSTANCES)
clf.fit(x_list, y_list)

# Calculate feature importance scores
importance_scores = clf.feature_importances_
print(importance_scores)
