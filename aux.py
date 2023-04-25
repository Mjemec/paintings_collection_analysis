import json
import os
import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
with open('by_group.json') as f:
    data = json.load(f)

keys = data[0]
pload = data[1]

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

    plt.plot(tmp[0], c='r')
    plt.plot(tmp[1], c='g')
    plt.plot(tmp[2], c='b')
    plt.title(e)
    plt.savefig(f'plots/{e}.png')

