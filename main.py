import random
import deeplake
import matplotlib.pyplot as plt
import filters
import datetime
import numpy as np
from sklearn.cluster import KMeans


def debug(msg):
    print(msg, datetime.datetime.now())


debug('load')
ds = deeplake.load('hub://activeloop/wiki-art')
i = 0
NUMBER_OF_INSTANCES = 3
debug("randomlist")
rand_list = random.sample(range(0, len(ds.images)), NUMBER_OF_INSTANCES)

x_list = list()
y_list = list()

for i in rand_list:
    debug('image')
    image = ds.images[i].numpy()
    debug('label')
    label = ds.labels[i].data()
    debug('filter')
    hist = filters.get_histogram(image)
    x_list.append(hist)
    y_list.append(label['text'])
    fig = plt.figure(figsize=(10, 7))
    fig.add_subplot(1, 2, 1)
    plt.imshow(image)
    fig.add_subplot(1, 2, 2)
    plt.plot(hist)
    plt.show()

kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(np.array(x_list))



pass
