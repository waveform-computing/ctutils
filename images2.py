# -*- coding: utf-8 -*-

#importing the operating system
import os
import scipy
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#change directory
os.chdir('E:/Callibration test scans/Bone test1 [2013-12-18 09.34.52]/Bone test1_BH3 Recon')

images1 = (
    scipy.misc.imread(f)
    for f in sorted(os.listdir('.'))[50:150]
    if f.endswith('.tif')
    )

counter1 = Counter()
for index, image in enumerate(images1):
    print('Processing image %d' % index)
    counter1.update(image.flatten())

#change directory
os.chdir('E:/Callibration test scans/Bone test after 220kv scans [2013-12-18 17.26.10]/Bone test after 220kv scans_recon')

images2 = (
    scipy.misc.imread(f)
    for f in sorted(os.listdir('.'))[50:150]
    if f.endswith('.tif')
    )

counter2 = Counter()
for index, image in enumerate(images2):
    print('Processing image %d' % index)
    counter2.update(image.flatten())

# calculate counts from each set of images
x1 = range(min(counter1.keys()), max(counter1.keys()) + 1)
x2 = range(min(counter2.keys()), max(counter2.keys()) + 1)
y1 = [counter1[i] for i in x1]
y2 = [counter2[i] for i in x2]

# plot the sets logarithmically
plt.semilogy(x1, y1, 'r', x2, y2, 'b')
plt.show()
