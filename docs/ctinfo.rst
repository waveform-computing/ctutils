.. _ctinfo:

======
ctinfo
======

This utility can be used to rapidly query the header of CT-scanner output in
various formats. Output is written to stdout in a format conducive to script
processing. File formats supported include TXM files (".txm"), VGI files
(".vgi" with an equivalently named ".vol" file), or TIFF stacks (specify one
of the TIFF filenames and all equivalently sized TIFFs in the directory will
be loaded as part of the stack).


Synopsis
========

::

    usage: ctinfo [-h] [--version] [-q] [-v] [-l FILE] [-P] input


Description
===========

.. program:: ctinfo

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


Examples
========

Output information about ``scan1.txm`` to the console::

    $ ctinfo scan1.txm

For each scan in the directory, write a text file detailing its contents::

    $ for f in *.vgi; do ctinfo $f > ${f%.vgi}.txt; done

Output information on all scans in a directory hierarchy::

    $ find -name "*.txm" -o -name "*.vgi" | xargs -n 1 ctinfo

