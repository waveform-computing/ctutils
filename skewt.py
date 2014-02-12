#!/usr/bin/env python

import io
import os
import sys
import csv
from collections import Counter

import scipy
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
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

cwd = os.getcwd()
#dir1 = QtGui.QFileDialog.getExistingDirectory(caption='Select dir 1')
#dir2 = QtGui.QFileDialog.getExistingDirectory(caption='Select dir 2')
dir1 = '/media/dave/My Passport/Callibration test scans/1st Run_16 bit unsigned/'
dir2 = '/media/dave/My Passport/Callibration test scans/2nd Run_16 bit unsigned/'

os.chdir(dir1)

images1 = (
    filename
    for filename in sorted(os.listdir('.'))
    if filename.endswith('.tif')
    )

counter1 = Counter()
for index, filename in enumerate(images1):
    with open(filename, 'rb') as f:
        image = scipy.misc.imread(f, flatten=True)
        print('Processing image %d' % index)
        counter1.update(image.flatten())

#change directory
os.chdir(dir2)

images2 = (
    filename
    for filename in sorted(os.listdir('.'))
    if filename.endswith('.tif')
    )

counter2 = Counter()
for index, filename in enumerate(images2):
    with open(filename, 'rb') as f:
        image = scipy.misc.imread(f, flatten=True)
        print('Processing image %d' % index)
        counter2.update(image.flatten())

os.chdir(cwd)

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

