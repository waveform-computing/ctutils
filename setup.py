#!/usr/bin/env python
# vim: set et sw=4 sts=4:

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )
str = type('')

import os
import sys
from setuptools import setup, find_packages

if sys.version_info[0] == 2:
    if not sys.version_info >= (2, 7):
        raise ValueError('This package requires Python 2.7 or above')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 2):
        raise ValueError('This package requires Python 3.2 or above')
else:
    raise ValueError('Unrecognized major version of Python')

HERE = os.path.abspath(os.path.dirname(__file__))

# Workaround <http://bugs.python.org/issue10945>
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

# Workaround <http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html>
try:
    import multiprocessing
except ImportError:
    pass

def main():
    import io
    import skewt as app
    with io.open(os.path.join(HERE, 'README.rst'), 'r') as readme:
        setup(
            name                 = app.__project__,
            version              = app.__version__,
            description          = app.__doc__,
            long_description     = readme.read(),
            classifiers          = app.__classifiers__,
            author               = app.__author__,
            author_email         = app.__author_email__,
            url                  = app.__url__,
            license              = [
                c.rsplit('::', 1)[1].strip()
                for c in app.__classifiers__
                if c.startswith('License ::')
                ][0],
            keywords             = ' '.join(app.__keywords__),
            packages             = find_packages(),
            package_data         = {},
            include_package_data = True,
            platforms            = app.__platforms__,
            install_requires     = app.__requires__,
            extras_require       = app.__extra_requires__,
            zip_safe             = True,
            entry_points         = app.__entry_points__,
            )

if __name__ == '__main__':
    main()
