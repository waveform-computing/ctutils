# vim: set et sw=4 sts=4 fileencoding=utf-8:

# Copyright 2014 Dave Hughes <dave@waveform.org.uk>.
#
# This file is part of skewt.
#
# skewt is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# skewt is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# skewt.  If not, see <http://www.gnu.org/licenses/>.

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
import csv
import argparse
import struct
import itertools
import logging
import collections

import compoundfiles
import numpy as np
from PIL import Image

from . import __version__
from .terminal import TerminalApplication, FileType
from .configparser import ConfigParser


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


def slice_str(s):
    return slice(*(
        int(x.strip()) if x.strip() else None
        for x in s.split(':')
        ))


class CtAggApplication(TerminalApplication):
    """
    This utility can be used to aggregate the density readings from all scans
    in a CT-scanner's output into a simple CSV file, suitable for plotting in a
    variety of applications. File formats supported include TXM files (".txm"),
    VGI files (".vgi" with an equivalently named ".vol" file), or TIFF stacks
    (specify one of the TIFF filenames and all equivalently sized TIFFs in the
    directory will be loaded as part of the stack). If no output filename is
    specified, output will be written to a file with the same name as the input
    but with a ".csv" extension.
    """

    def __init__(self):
        super(CtAggApplication, self).__init__(
            version=__version__,
            config_files=[],
            )
        self.parser.add_argument(
            '-s', '--slice', type=slice_str, default=slice(None),
            metavar='START[:STOP[:STEP]]',
            help='specifies the index(es) of image(s) to extract from the '
            'scan in Python slice notation, e.g. 0:50 to extract the first 50 '
            'images, 50: to extract all images from the 50th onward, or '
            '::5 to extract every 5th image. Defaults to all images')
        self.parser.add_argument(
            '-f', '--filter', type=int, default=1, metavar='NUM',
            help='any counts below the specified filter level will be '
            'excluded from the CSV output')
        self.parser.add_argument('input', type=FileType('rb'))
        if sys.version_info[0] == 3:
            self.parser.add_argument('output', nargs='?', type=FileType('w', newline=''))
        else:
            self.parser.add_argument('output', nargs='?', type=FileType('wb'))

    def main(self, args):
        try:
            cls = {
                '.txm': TxmScanReader,
                '.vgi': VgiScanReader,
                '.tif': TiffStackReader,
                '.tiff': TiffStackReader,
                }[os.path.splitext(args.input.name.lower())[1]]
        except KeyError:
            raise argparse.ArgumentError(
                'Unrecognized file type: %s' % args.input.name)
        logging.info('Parsing input %s', args.input.name)
        reader = cls(args.input)
        logging.info('Input format is "%s"', reader.format_name)
        logging.info('Input resolution is %dx%d', reader.width, reader.height)
        logging.info('Input datatype is %s', reader.datatype().dtype.name)
        logging.info('Input contains %d images', len(reader))
        if not args.output:
            filename = ''.join((os.path.splitext(args.input.name)[0], '.csv'))
            if sys.version_info[0] == 3:
                args.output = io.open(filename, 'w', newline='')
        logging.info('Writing output to %s', args.output.name)
        writer = csv.writer(args.output)
        counter = collections.Counter()
        for scan in itertools.islice(
                reader, args.slice.start, args.slice.stop, args.slice.step):
            logging.info('Aggregating scan %s', scan)
            data = reader[scan]
            if reader.datatype in (np.float32, np.float64):
                data = data.astype(np.int32)
            counter.update(data)
        x_min = min(counter.keys())
        x_max = max(counter.keys())
        logging.info('Density range: %d to %d', x_min, x_max)
        for (x, y) in sorted(counter.items()):
            if y >= args.filter:
                writer.writerow((x, y))


main = CtAggApplication()
