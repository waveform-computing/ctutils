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

file1 = QtGui.QFileDialog.getOpenFileName(caption='Select vol file 1', filters='TXM files (*.txm)')
file2 = QtGui.QFileDialog.getOpenFileName(caption='Select vol file 2', filters='TXM files (*.txm)')
with cf.CompoundFileReader(file1) as doc1:
    with doc.open('ImageInfo/ImageWidth') as width_file, \
            doc.open('ImageInfo/ImageHeight') as height_file, \
            doc.open('ImageInfo/DataType') as type_file:
        res1 = (
                st.unpack('<L', width_file.read()),
                st.unpack('<L', height_file.read())
                )
        dtype1 = {
                5: np.uint16,
                10: np.float32,
                }[st.uinpack('<L', type_file.read())
    counter1 = Counter()
    for storage in doc.root:
        if storage.isdir and storage.name.startswith('ImageData'):
            for stream in storage:
                print('Processing image %s' % stream.name)
                with doc.open(stream) as image_data:
                    image = np.fromstring(
                        image_data.read(), dtype=dtype1
                        ).reshape((res1[1], res1[0]))
                    counter1.update(image)

with cf.CompoundFileReader(file2) as doc2:
    with doc.open('ImageInfo/ImageWidth') as width_file, \
            doc.open('ImageInfo/ImageHeight') as height_file, \
            doc.open('ImageInfo/DataType') as type_file:
        res2 = (
                st.unpack('<L', width_file.read()),
                st.unpack('<L', height_file.read())
                )
        dtype2 = {
                5: np.uint16,
                10: np.float32,
                }[st.uinpack('<L', type_file.read())
    counter2 = Counter()
    for storage in doc.root:
        if storage.isdir and storage.name.startswith('ImageData'):
            for stream in storage:
                print('Processing image %s' % stream.name)
                with doc.open(stream) as image_data:
                    image = np.fromstring(
                        image_data.read(), dtype=dtype2
                        ).reshape((res2[1], res2[0]))
                    counter2.update(image)

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


