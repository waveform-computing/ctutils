# vim: set et sw=4 sts=4 fileencoding=utf-8:

# Copyright 2014 Dave Hughes <dave@waveform.org.uk>.
#
# This file is part of ctutils.
#
# ctutils is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ctutils is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# ctutils.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
native_str = str
str = type('')
try:
    range = xrange
except NameError:
    pass

import sys
import os
import io
import struct

import compoundfiles
import numpy as np
from PIL import Image


class TxmScanReader(object):
    format_name = 'Xradia TXM format'

    def __init__(self, source):
        super(TxmScanReader, self).__init__()
        self._data = compoundfiles.CompoundFileReader(source)
        self.width = struct.unpack(
            native_str('<L'),
            self._data.open('/ImageInfo/ImageWidth').read())[0]
        self.height = struct.unpack(
            native_str('<L'),
            self._data.open('/ImageInfo/ImageHeight').read())[0]
        datatype = struct.unpack(
            native_str('<L'),
            self._data.open('/ImageInfo/DataType').read())[0]
        try:
            self.datatype = {
                5:  np.uint16,
                10: np.float32,
                }[datatype]
        except KeyError:
            raise IOError('Unrecognized datatype in TXM file: %d' % datatype)

    def __len__(self):
        return struct.unpack(
            native_str('<L'),
            self._data.open('/ImageInfo/ImagesTaken').read())[0]

    def __iter__(self):
        for storage in self._data.root:
            if storage.isdir and storage.name.startswith('ImageData'):
                for stream in storage:
                    if stream.isfile and stream.name.startswith('Image'):
                        yield '/%s/%s' % (storage.name, stream.name)

    def __getitem__(self, key):
        try:
            with self._data.open(key) as data:
                return np.fromstring(data.read(), dtype=self.datatype)
        except compoundfiles.CompoundFileError:
            raise KeyError(key)


class VgiScanReader(object):
    format_name = 'VGI ???'

    def __init__(self, source):
        super(VgiScanReader, self).__init__()
        # Copy the {volume1} section into a private stream for parsing
        config = io.StringIO()
        copying = False
        for line in source:
            line = line.decode('latin-1').strip()
            if copying:
                if line.startswith('{'):
                    break
                config.write(line + '\r\n')
            elif line == '{volume1}':
                copying = True
        config.seek(0)
        parser = ConfigParser(interpolation=None)
        parser.readfp(config)
        size = parser.get('representation', 'size')
        self.width, self.height, self._len = (int(i) for i in size.split())
        datatype = parser.get('representation', 'datatype')
        databits = parser.get('representation', 'bitsperelement')
        try:
            self.datatype = {
                ('float', '32'): np.float32,
                ('float', '64'): np.float64,
                }[(datatype, databits)]
        except KeyError:
            raise IOError(
                'Unrecognized datatype in VGI file: %s %s' % (datatype, databits))
        if sys.version_info[0] == 3:
            self._data = io.open(source.name.replace('.vgi', '.vol'), 'rb')
        else:
            self._data = open(source.name.replace('.vgi', '.vol'), 'rb')

    def __len__(self):
        return self._len

    def __iter__(self):
        for i in range(self._len):
            yield i

    def __getitem__(self, key):
        if not key in range(self._len):
            raise KeyError(key)
        count = self.width * self.height
        self._data.seek(count * self.datatype().nbytes * key)
        return np.fromfile(self._data, dtype=self.datatype, count=count)


class TiffStackReader(object):
    format_name = 'Generic TIFF stack'

    def __init__(self, source):
        super(TiffStackReader, self).__init__()
        sample = Image.open(source)
        self.width, self.height = sample.size
        try:
            self.datatype = {
                'I;16': np.uint16,
                }[sample.mode]
        except KeyError:
            raise IOError('Unrecognized TIFF mode: %s' % sample.mode)
        self._data = []
        path, name = os.path.split(source.name)
        ext = os.path.splitext(name)[1]
        for filename in os.listdir(path):
            if os.path.splitext(filename)[1] == ext:
                filename = os.path.join(path, filename)
                test = Image.open(filename)
                if test.size == sample.size and test.mode == sample.mode:
                    self._data.append(filename)
        self._data = sorted(self._data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        if not key in self._data:
            raise KeyError(key)
        img = Image.open(key)
        return np.fromiter(img.getdata(), dtype=self.datatype)


