# -*- coding: utf-8 -*-

#importing the operating system
import os
import io
import csv
import scipy
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#change directory
os.chdir('E:/Callibration test scans/1st Run_16 bit unsigned')

images1 = (
    scipy.misc.imread(f)
    for f in sorted(os.listdir('.'))
    if f.endswith('.tif')
    )
    
counter1 = Counter()
for index, image in enumerate(images1):
    print('Processing image %d' % index)
    counter1.update(image.flatten())
    
#change directory
os.chdir('E:/Callibration test scans/2nd Run_16 bit unsigned')

images2 = (
    scipy.misc.imread(f)
    for f in sorted(os.listdir('.'))
    if f.endswith('.tif')
    )
    
counter2 = Counter()
for index, image in enumerate(images2):
    print('Processing image %d' % index)
    counter2.update(image.flatten())

# calculate counts from each set of images
with io.open('data1.csv', 'wb') as f:
    w = csv.writer(f)
    for x, y in counter1.items():
        w.writerow((x, y))
        
with io.open('data2.csv', 'wb') as f:
    w = csv.writer(f)
    for x, y in counter2.items():
        w.writerow((x, y))
        
x1 = sorted(counter1.keys())
x2 = sorted(counter2.keys())

y1 = [counter1[i] for i in x1]
y2 = [counter2[i] for i in x2]

y_max1 = max(counter1.values())
y_max2 = max(counter2.values())

x_max1 = [x for x, y in counter1.items() if y == y_max1][0]
x_max2 = [x for x, y in counter2.items() if y == y_max2][0]

print(x_max1, y_max1)
print(x_max2, y_max2)

# plot the sets logarithmically
plt.semilogy(x1, y1, 'r', x2, y2, 'b')
plt.show()
