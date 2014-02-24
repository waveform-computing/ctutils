#!/usr/bin/env python

from __future__ import division

import io
import os
import sys
from collections import Counter

import scipy
import scipy.misc
import numpy as np
import struct as st
import matplotlib.pyplot as plot
try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    from PySide import QtCore, QtGui, uic
from compoundfiles import CompoundFileReader

APPLICATION = None
MAIN_WINDOW = None

APPLICATION = QtGui.QApplication(sys.argv)
APPLICATION.setApplicationName('Skewt')
APPLICATION.setApplicationVersion('0.1')
APPLICATION.setOrganizationName('Waveform')
APPLICATION.setOrganizationDomain('waveform.org.uk')

file1 = str(QtGui.QFileDialog.getOpenFileName(caption='Select vol file 1', filter='TXM files (*.txm)'))
if not file1:
    raise ValueError('Terminated by user')
with CompoundFileReader(file1) as doc1:
    with doc1.open('ImageInfo/ImageWidth') as width_file:
        width1 = st.unpack('<L', width_file.read())[0]
    with doc1.open('ImageInfo/ImageHeight') as height_file:
        height1 = st.unpack('<L', height_file.read())[0]
    with doc1.open('ImageInfo/DataType') as type_file:
        dtype1 = st.unpack('<L', type_file.read())[0]
    res1 = (width1, height1)
    dtype1 = {
            5: np.uint16,
            10: np.float32,
            }[dtype1]
    counter1 = Counter()
    for storage in doc1.root:
        if storage.isdir and storage.name.startswith('ImageData'):
            for stream in storage:
                print('Processing image %s' % stream.name)
                with doc1.open(stream) as image_data:
                    image = np.fromstring(
                        image_data.read(), dtype=dtype1
                        ).reshape((height1, width1))
                    counter1.update(image.flatten())

file2 = str(QtGui.QFileDialog.getOpenFileName(caption='Select vol file 2', filter='TXM files (*.txm)'))
if not file2:
    raise ValueError('Terminated by user')
with CompoundFileReader(file2) as doc2:
    with doc2.open('ImageInfo/ImageWidth') as width_file:
        width2 = st.unpack('<L', width_file.read())[0]
    with doc2.open('ImageInfo/ImageHeight') as height_file:
        height2 = st.unpack('<L', height_file.read())[0]
    with doc2.open('ImageInfo/DataType') as type_file:
        dtype2 = st.unpack('<L', type_file.read())[0]
    res2 = (width2, height2)
    dtype2 = {
            5: np.uint16,
            10: np.float32,
            }[dtype2]
    counter2 = Counter()
    for storage in doc2.root:
        if storage.isdir and storage.name.startswith('ImageData'):
            for stream in storage:
                print('Processing image %s' % stream.name)
                with doc2.open(stream) as image_data:
                    image = np.fromstring(
                        image_data.read(), dtype=dtype2
                        ).reshape((height2, width2))
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


