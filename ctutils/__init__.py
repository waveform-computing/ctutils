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

"Tools for analyzing data in CT scans"

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
str = type('')

import sys

__project__      = 'ctutils'
__version__      = '0.3'
__author__       = 'Dave Hughes'
__author_email__ = 'dave@waveform.org.uk'
__url__          = 'http://ctutils.readthedocs.org/'
__platforms__    = 'ALL'

__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Visualization',
    ]

__keywords__ = [
    'ct',
    'tomography',
    ]

__requires__ = [
    'compoundfiles',
    'numpy',
    'Pillow',
    ]

__extra_requires__ = {
    'doc': ['sphinx'],
    'test': ['pytest', 'coverage', 'mock'],
    'GUI': ['pyqt'],
    }

if sys.version_info[:2] == (3, 2):
    __extra_requires__['doc'].extend([
        # Particular versions are required for Python 3.2 compatibility. The
        # ordering is reversed because that's what easy_install needs...
        'Jinja2<2.7',
        'MarkupSafe<0.16',
        ])

__entry_points__ = {
    'console_scripts': [
        'ctagg = ctutils.ctagg:main',
        'ctinfo = ctutils.ctinfo:main',
        #'ctstack = ctutils.ctstack:main',
        ],
    'gui_scripts': [
        #'ctview = ctutils.ctview:main',
        ]
    }


