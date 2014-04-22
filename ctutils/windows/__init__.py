# -*- coding: utf-8 -*-
# vim: set et sw=4 sts=4:

"Utility routines for GUI applications using pkg_resources"

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )
str = type('')

import sys
import os

try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    from PySide import QtCore, QtGui, uic


if getattr(sys, 'frozen', None):
    def get_ui_dir():
        "Returns the directory containing the *.ui Qt window definitions"
        result = os.path.abspath(os.path.join(
            os.path.dirname(sys.executable), *__name__.split('.')))
        # Check the result is a directory and that it contains at least one .ui file
        if not os.path.isdir(result):
            raise ValueError('Expected %s to be a directory' % result)
        if not any(filename.endswith('.ui') for filename in os.listdir(result)):
            raise ValueError('UI directory %s does not contain any .ui files' % result)
        return result

    UI_DIR = get_ui_dir()

    def resource_exists(module, name):
        name = os.path.join(UI_DIR, name)
        return os.path.exists(name) and not os.path.isdir(name)

    def resource_stream(module, name):
        name = os.path.join(UI_DIR, name)
        return open(name, 'r')

    def resource_filename(module, name):
        name = os.path.join(UI_DIR, name)
        return name
else:
    from pkg_resources import resource_stream, resource_filename, resource_exists


def get_ui_file(ui_file):
    "Returns a file-like object for the specified .ui file"
    return resource_stream(__name__, ui_file)

def get_icon(icon_id):
    "Returns an icon from the system theme or our fallback theme if required"
    fallback_path = os.path.join('fallback-theme', icon_id + '.png')
    if resource_exists(__name__, fallback_path):
        return QtGui.QIcon.fromTheme(icon_id,
            QtGui.QIcon(resource_filename(__name__, fallback_path)))
    else:
        return QtGui.QIcon.fromTheme(icon_id)

