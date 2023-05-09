import json
import os
import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
with open('by_group.json') as f:
    data = json.load(f)

keys = data[0]
pload = data[1]
lines = []
faces = []
people = []
contours = []
for e in pload:
    lines.append(pload[e][-4])
    faces.append(pload[e][-3])
    people.append(pload[e][-2])
    contours.append(pload[e][-1])

for i, line in enumerate(lines):
    plt.bar(keys[i], line)

os.makedirs('time_plots', exist_ok=True)

plt.xticks(rotation=90)
plt.title('lines')
plt.subplots_adjust(top=0.9, bottom=0.4, left=0.1, right=0.9)
plt.savefig('time_plots/lines.png')
plt.cla()
plt.clf()

for i, peopl in enumerate(people):
    plt.bar(keys[i], peopl)

plt.xticks(rotation=90)
plt.title('people')
plt.subplots_adjust(top=0.9, bottom=0.4, left=0.1, right=0.9)
plt.savefig('time_plots/people.png')
plt.cla()
plt.clf()

for i, cont in enumerate(contours):
    plt.bar(keys[i], cont)

plt.xticks(rotation=90)
plt.title('contours')
plt.subplots_adjust(top=0.9, bottom=0.4, left=0.1, right=0.9)
plt.savefig('time_plots/contours.png')
plt.cla()
plt.clf()

for i, line in enumerate(faces):
    plt.bar(keys[i], line)

plt.xticks(rotation=90)
plt.title('faces')
plt.subplots_adjust(top=0.9, bottom=0.4, left=0.1, right=0.9)
plt.savefig('time_plots/faces.png')
plt.cla()
plt.clf()

arr = list(pload.values())
arr = np.array(arr)
arr = arr/arr.max(axis=0)
pca = PCA(n_components=2)
pca.fit(arr)
t = pca.transform(arr)

for index, e in enumerate(t):
    plt.scatter(e[0], e[1])
    plt.text(e[0], e[1], keys[index])

plt.show()


histograms = dict()

with open('raw.json') as f:
    data = json.load(f)

for e in data:
    if e[2] in histograms.keys():
        histograms[e[2]].append(e[0])
    else:
        histograms[e[2]] = [e[0]]
try:
    os.mkdir('plots')
except:
    pass

for e in histograms.keys():
    tmp = np.array(histograms[e])/len(histograms[e])
    tmp = tmp.mean(axis=0)
    plt.clf()
    plt.cla()
    plt.plot(tmp[0], c='r')
    plt.plot(tmp[1], c='g')
    plt.plot(tmp[2], c='b')
    plt.title(e)
    plt.savefig(f'plots/{e}.png')

