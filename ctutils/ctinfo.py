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
str = type('')

import logging

from . import __version__
from .terminal import TerminalApplication, FileType
from .readers import open_scan

class CtInfoApplication(TerminalApplication):
    """
    This utility can be used to rapidly query the header of CT-scanner output
    in various formats. Output is written to stdout in a format conducive to
    script processing. File formats supported include TXM files (".txm"),
    VGI files (".vgi" with an equivalently named ".vol" file), or TIFF stacks
    (specify one of the TIFF filenames and all equivalently sized TIFFs in the
    directory will be loaded as part of the stack).
    """

    def __init__(self):
        super(CtInfoApplication, self).__init__(
            version=__version__,
            config_files=[],
            )
        self.parser.add_argument('input', type=FileType('rb'))

    def main(self, args):
        print('Filename: %s' % args.input.name)
        reader = open_scan(args.input)
        print('Input format: %s' % reader.format_name)
        print('Input resolution: %dx%d' % (reader.width, reader.height))
        print('Input datatype: %s' % reader.datatype().dtype.name)
        print('Input images: %d' % len(reader))


main = CtInfoApplication()
