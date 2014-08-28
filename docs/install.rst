.. _install:

============
Installation
============

CT Utils is designed to be cross platform and should work happily on Microsoft
Windows (under a variety of different Python frameworks), Mac OS X, and Linux.
The following sections detail installation in these different environments.


Ubuntu Linux
============

The simplest method of installation under Ubuntu is to use the author's PPA
as a source::

$ sudo add-apt-repository ppa:waveform/ppa
$ sudo apt-get update
$ sudo apt-get install ctutils

This will ensure that CT Utils remains up to date through the usual apt upgrade
system. To remove the installation::

$ sudo apt-get remove ctutils


Other Linux
===========

Ensure you have Python's setuptools and pip packages installed, then run the
following command::

$ sudo pip install ctutils

To upgrade your installation after new releases::

$ sudo pip install -U ctutils

To remove your installation::

$ sudo pip uninstall ctutils


Windows with Python(x,y)
========================

Start a command window (note: not a Python console) and run the following
command::

$ pip install ctutils

To upgrade your installation after new releases::

$ pip install -U ctutils

To remove your installation::

$ sudo pip uninstall ctutils

.. note::

    Please note that Python(x,y) is only a 32-bit installation. As CT Utils
    relies on memory mapping for handling large files, operating on files
    larger than 2Gb will fail in the current version. Future versions may
    incorporate an emulation to work around this but operation will be
    considerably slower than simply using a 64-bit installation.


Windows with Canopy
===================

This installation assumes you configured Canopy as your system Python
installation. Start a windows command prompt (Win+R, ``cmd``) and run the
following commands::

$ pip uninstall PIL
$ pip install Pillow
$ pip install ctutils

The reason for replacing PIL (the Python Imaging Library) with Pillow is that
PIL is effectively unmaintained at this point. Pillow is a fork of the PIL
project which is carrying on maintenance and providing Python 3 compatibility.

To upgrade your installation after new releases::

$ pip install -U ctutils

To remove your installation::

$ sudo pip uninstall ctutils


Windows with Anaconda
=====================

This installation assumes you configured Anaconda as your system Python
installation. Start a windows command prompt (Win+R, ``cmd``) and run the
following commands::

$ pip install -U argcomplete
$ pip install ctutils

Anaconda ships with a slightly out of date argcomplete package (CT Utils
assumes version 0.7 or above if it finds argcomplete installed) which requires
upgrading. This is a rather moot point on Windows however, as argcomplete
relies on bash/zsh for its functionality and won't work under a regular Windows
cmd shell.

To upgrade your installation after new releases::

$ pip install -U ctutils

To remove your installation::

$ sudo pip uninstall ctutils

