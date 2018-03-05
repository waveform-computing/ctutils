.. _ctagg:

=====
ctagg
=====

This utility can be used to aggregate the density readings from all scans in a
CT-scanner's output into a simple CSV file, suitable for plotting in a variety
of applications. File formats supported include TXM files (".txm"), VGI files
(".vgi" with an equivalently named ".vol" file), or TIFF stacks (specify one
of the TIFF filenames and all equivalently sized TIFFs in the directory will
be loaded as part of the stack). If no output filename is specified, output
will be written to a file with the same name as the input but with a ".csv"
extension.


Synopsis
========

::

    ctagg [-h] [--version] [-q] [-v] [-l FILE] [-P]
          [-s START[:STOP[:STEP]]] [-f NUM]
          input [output]


Description
===========

.. program:: ctagg

.. option:: -h, --help

    show this help message and exit

.. option:: --version

    show program's version number and exit

.. option:: -q, --quiet

    produce less console output

.. option:: -v, --verbose

    produce more console output

.. option::  -l FILE, --log-file FILE

    log messages to the specified file

.. option:: -P, --pdb

    run under PDB (debug mode)

.. option:: -s START[:STOP[:STEP]], --slice START[:STOP[:STEP]]

    specifies the index(es) of image(s) to extract from the scan in Python
    slice notation, e.g. ``0:50`` to extract the first 50 images, ``50:`` to
    extract all images from the 50th onward, or ``::5`` to extract every 5th
    image.  Defaults to all images

.. option:: -f NUM, --filter NUM

    any counts below the specified filter level will be excluded from the CSV
    output


Examples
========

Extract all density measurements from ``scan1.txm`` into ``scan1.csv``::

    $ ctagg scan1.txm

Extract density measurements from every 10th slice in ``scan1.txm`` into
``preview.csv``::

    $ ctagg --slice ::10 scan1.txm preview.csv

Extract density measurements from the first slice in ``scan1.vgi`` into
``first.csv`` (this assumes a corresponding file named ``scan1.vol`` exists in
the same directory as ``scan1.vgi``)::

    $ ctagg --slice :1 scan1.vgi first.csv

Extract density measurements from every third slice of the TIFF stack which
includes ``slice001.tiff``, ignoring densities below 10 into ``quick.csv``,
printing verbose progress messages to the console::

    $ ctagg -v --slice ::3 --filter 10 slice001.tiff preview.csv

When processing TIFF stacks, simply specify the name of one of the TIFF images
in the stack. The utility will automatically locate all other TIFF images that
exist in the same directory and which have the same resolution as the specified
TIFF. The images will be arranged in the stack in alphabetical order by
filename.


Known Issues
============

Our understanding of several of the formats above is limited (in particular TXM
and VGI+VOL), specifically in terms of the data types supported within these
files. If you encounter a file which does not work with CT Utils, please file a
`bug report`_ so that we can enhance the suite.

.. _bug report: https://github.com/waveform-computing/ctutils/issues

