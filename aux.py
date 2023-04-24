import json
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

for index,e in enumerate(t):
    plt.scatter(e[0], e[1])
    plt.text(e[0], e[1], keys[index])
plt.show()
