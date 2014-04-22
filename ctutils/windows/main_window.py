# -*- coding: utf-8 -*-
# vim: set et sw=4 sts=4:

"Module implementing the ctutils main window."

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )
str = type('')

import io
import os

try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    from PySide import QtCore, QtGui, uic

from ctutils.windows import get_icon, get_ui_file


class MainWindow(QtGui.QMainWindow):
    "The ctutils main window"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dummy_logger = None
        self.ui = uic.loadUi(get_ui_file('main_window.ui'), self)
        # Read configuration
        self.settings = QtCore.QSettings()
        self.settings.beginGroup('main_window')
        try:
            self.resize(
                self.settings.value(
                    'size', QtCore.QSize(640, 480)))
            self.move(
                self.settings.value(
                    'position', QtCore.QPoint(100, 100)))
        finally:
            self.settings.endGroup()
        # Configure status bar elements
        self.ui.progress_label = QtGui.QLabel('')
        self.statusBar().addWidget(self.ui.progress_label)
        self.progress_index = 0
        self.ui.quit_action.setIcon(get_icon('application-exit'))
        self.ui.about_action.triggered.connect(self.about)
        self.ui.about_action.setIcon(get_icon('help-about'))
        self.ui.about_qt_action.triggered.connect(self.about_qt)
        self.ui.about_qt_action.setIcon(get_icon('help-about'))
        self.ui.status_bar_action.triggered.connect(self.toggle_status)
        self.ui.view_menu.aboutToShow.connect(self.update_status)

    def close(self):
        "Called when the window is closed"
        self.settings.beginGroup('main_window')
        try:
            self.settings.setValue('size', self.size())
            self.settings.setValue('position', self.pos())
        finally:
            self.settings.endGroup()
        super(MainWindow, self).close()

    def update_status(self):
        "Called to update the status_bar_action check state"
        self.ui.status_bar_action.setChecked(self.statusBar().isVisible())

    def toggle_status(self):
        "Handler for the View/Status Bar action"
        if self.statusBar().isVisible():
            self.statusBar().hide()
        else:
            self.statusBar().show()

    def about(self):
        "Handler for the Help/About action"
        QtGui.QMessageBox.about(self,
            str(self.tr('About {}')).format(
                QtGui.QApplication.instance().applicationName()),
            str(self.tr("""\
<b>{application}</b>
<p>Version {version}</p>
<p>{application} is a GUI for skew analysis of CT scans.
Project homepage is at
<a href="{url}">{url}</a></p>
<p>Copyright &copy; 2012-2013 {author} &lt;<a href="mailto:{author_email}">{author_email}</a>&gt;</p>""")).format(
                application=QtGui.QApplication.instance().applicationName(),
                version=QtGui.QApplication.instance().applicationVersion(),
                url='https://www.waveform.org.uk/ctutils/',
                author='Dave Hughes',
                author_email='dave@waveform.org.uk',
            ))

    def about_qt(self):
        "Handler for the Help/About Qt action"
        QtGui.QMessageBox.aboutQt(self, self.tr('About Qt'))

    def progress_start(self):
        QtGui.QApplication.instance().setOverrideCursor(QtCore.Qt.WaitCursor)

    def progress_update(self):
        self.progress_index += 1
        self.ui.progress_label.setText('Working' + '.' * (self.progress_index % 8))
        QtGui.QApplication.instance().processEvents()

    def progress_finish(self):
        self.ui.progress_label.setText('')
        QtGui.QApplication.instance().restoreOverrideCursor()

