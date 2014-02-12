#!/usr/bin/env python

from __future__ import division

import io
import os
import sys
from collections import Counter

import scipy
import scipy.misc
import numpy as np
import matplotlib.pyplot as plot
try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    from PySide import QtCore, QtGui, uic

APPLICATION = None
MAIN_WINDOW = None

APPLICATION = QtGui.QApplication(sys.argv)
APPLICATION.setApplicationName('Skewt')
APPLICATION.setApplicationVersion('0.1')
APPLICATION.setOrganizationName('Waveform')
APPLICATION.setOrganizationDomain('waveform.org.uk')

file1 = QtGui.QFileDialog.getOpenFileName(caption='Select vol file 1', filters='Vol files (*.vol)')
res1 = (1920, 1080)
file2 = QtGui.QFileDialog.getOpenFileName(caption='Select vol file 2', filters='Vol files (*.vol)')
res2 = (1920, 1080)

with io.open(file1, 'rb') as f1:
    count = f1.seek(0, io.SEEK_END) // (res1[0] * res1[1])
    assert count * res1[0] * res1[1] == f1.tell()
    f1.seek(0)
    images1 = (
        np.fromfile(f1, dtype=np.uint8, count=res1[0] * res1[1]).reshape((res1[1], res1[0]))
        for i in range(count)
        )

    counter1 = Counter()
    for index, image in enumerate(images1):
        print('Processing image %d' % index)
        counter1.update(image.flatten())

with io.open(file2, 'rb') as f2:
    count = f2.seek(0, io.SEEK_END) // (res2[0] * res2[1])
    assert count * res2[0] * res2[1] == f2.tell()
    f2.seek(0)
    images2 = (
        np.fromfile(f2, dtype=np.uint8, count=res2[0] * res2[1]).reshape((res2[1], res2[0]))
        for f in range(count)
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


