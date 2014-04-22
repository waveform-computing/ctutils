"Tools for analyzing skew in CT scans"

import sys

__project__      = 'skewt'
__version__      = '0.1'
__author__       = 'Dave Hughes'
__author_email__ = 'dave@waveform.org.uk'
__url__          = 'http://pypi.python.org/pypi/skewt'
__platforms__    = ['ALL']

__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Scientific/Engineering :: Visualization',
    ]

__keywords__ = [
    'ct',
    'skew',
    ]

__requires__ = [
    'compoundfiles',
    'numpy',
    'Pillow',
    ]

__extra_requires__ = {
    'doc': ['sphinx'],
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
        'ctagg = skewt.ctagg:main',
        ],
    'gui_scripts': [
        #'skewt = skewt.skewt:main',
        ]
    }


