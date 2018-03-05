# vim: set et sw=4 sts=4 fileencoding=utf-8:

# Copyright 2014 Dave Jones <dave@waveform.org.uk>.
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
str = type('')

import sys
PY3 = sys.version_info[0] == 3
import os
import io
import csv
import argparse
import itertools
import logging
import collections

import numpy as np

from . import __version__
from .terminal import TerminalApplication, FileType
from .readers import open_scan


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
        if PY3:
            self.parser.add_argument('output', nargs='?', type=FileType('w', newline=''))
        else:
            self.parser.add_argument('output', nargs='?', type=FileType('wb'))

    def main(self, args):
        logging.info('Parsing input %s', args.input.name)
        reader = open_scan(args.input)
        logging.info('Input format: %s', reader.format_name)
        logging.info('Input resolution: %dx%d', reader.width, reader.height)
        logging.info('Input datatype: %s', reader.datatype().dtype.name)
        logging.info('Input images: %d', len(reader))
        if not args.output:
            filename = ''.join((os.path.splitext(args.input.name)[0], '.csv'))
            if PY3:
                args.output = io.open(filename, 'w', newline='')
            else:
                args.output = io.open(filename, 'wb')
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
