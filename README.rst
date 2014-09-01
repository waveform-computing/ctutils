========
CT Utils
========

This project provides a set (currently one!) of small utilities for processing
data from CT scanners in a variety of formats. Currently, the supported formats
are:

* Xradia's TXM format
* Volume Graphics VGI+VOL format
* Grayscale TIFF stacks (8-bit, 16-bit)

At the moment, the project's goal is to produce a set of simple command line
tools for batch processing of CT scans, and an API to permit easy access to
scan data from Python.

.. note::

    Please note that our understanding of several of the formats above is
    limited (in particular TXM and VGI+VOL), specifically in terms of the data
    types supported within these files.

    If you encounter a file which does not work with CT Utils, please file a
    `bug report <bug tracker>`_ so that we can enhance the suite. Obviously
    example files make debugging easier, but we understand there may be
    confidentiality issues with certain scans (publication embargoes, medical
    privacy, etc.). If this applies to your scans, please do not attach them to
    the bug report!

Links
=====

* The project is licensed under the `GPL v3`_ or above
* Project `source code`_ is hosted by GitHub which also hosts the `bug tracker`_
* The `documentation`_ is hosted by ReadTheDocs

.. _documentation: http://ctutils.readthedocs.org/
.. _source code: https://github.com/waveform80/ctutils
.. _bug tracker: https://github.com/waveform80/ctutils/issues
.. _GPL v3: https://www.gnu.org/licenses/gpl-3.0.html

