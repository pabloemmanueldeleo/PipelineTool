# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX\uiExocortex.ui'
#
# Created: Tue Dec 29 19:36:36 2015
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PH_EXOCORTEX(object):
    def setupUi(self, PH_EXOCORTEX):
        PH_EXOCORTEX.setObjectName("PH_EXOCORTEX")
        PH_EXOCORTEX.resize(597, 377)
        self.COLUMNA = QtGui.QWidget(PH_EXOCORTEX)
        self.COLUMNA.setObjectName("COLUMNA")
        self.TABS = QtGui.QTabWidget(self.COLUMNA)
        self.TABS.setGeometry(QtCore.QRect(10, 10, 311, 341))
        font = QtGui.QFont()
        font.setFamily("Raavi")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.TABS.setFont(font)
        self.TABS.setObjectName("TABS")
        self.CHANGE = QtGui.QWidget()
        self.CHANGE.setObjectName("CHANGE")
        self.label = QtGui.QLabel(self.CHANGE)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Raavi")
        font.setPointSize(14)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.BTN_CHANGE = QtGui.QPushButton(self.CHANGE)
        self.BTN_CHANGE.setGeometry(QtCore.QRect(10, 220, 281, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BTN_CHANGE.setFont(font)
        self.BTN_CHANGE.setObjectName("BTN_CHANGE")
        self.EXONODOS = QtGui.QListView(self.CHANGE)
        self.EXONODOS.setGeometry(QtCore.QRect(10, 30, 281, 181))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.EXONODOS.setFont(font)
        self.EXONODOS.setObjectName("EXONODOS")
        self.TABS.addTab(self.CHANGE, "")
        self.EXPORTAB = QtGui.QWidget()
        self.EXPORTAB.setObjectName("EXPORTAB")
        self.TABS.addTab(self.EXPORTAB, "")
        self.IMPORTAB = QtGui.QWidget()
        self.IMPORTAB.setObjectName("IMPORTAB")
        self.TABS.addTab(self.IMPORTAB, "")
        self.ABOUT = QtGui.QWidget()
        self.ABOUT.setObjectName("ABOUT")
        self.TABS.addTab(self.ABOUT, "")
        PH_EXOCORTEX.setCentralWidget(self.COLUMNA)
        self.statusbar = QtGui.QStatusBar(PH_EXOCORTEX)
        self.statusbar.setObjectName("statusbar")
        PH_EXOCORTEX.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(PH_EXOCORTEX)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(PH_EXOCORTEX)
        self.TABS.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PH_EXOCORTEX)

    def retranslateUi(self, PH_EXOCORTEX):
        PH_EXOCORTEX.setWindowTitle(QtGui.QApplication.translate("PH_EXOCORTEX", "PH_EXOCORTEX", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PH_EXOCORTEX", "Lista de Exocortex en escena:", None, QtGui.QApplication.UnicodeUTF8))
        self.BTN_CHANGE.setText(QtGui.QApplication.translate("PH_EXOCORTEX", "RELOAD ANIMATION", None, QtGui.QApplication.UnicodeUTF8))
        self.TABS.setTabText(self.TABS.indexOf(self.CHANGE), QtGui.QApplication.translate("PH_EXOCORTEX", "CHANGE", None, QtGui.QApplication.UnicodeUTF8))
        self.TABS.setTabText(self.TABS.indexOf(self.EXPORTAB), QtGui.QApplication.translate("PH_EXOCORTEX", "EXPORT", None, QtGui.QApplication.UnicodeUTF8))
        self.TABS.setTabText(self.TABS.indexOf(self.IMPORTAB), QtGui.QApplication.translate("PH_EXOCORTEX", "IMPORT", None, QtGui.QApplication.UnicodeUTF8))
        self.TABS.setTabText(self.TABS.indexOf(self.ABOUT), QtGui.QApplication.translate("PH_EXOCORTEX", "ABOUT", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("PH_EXOCORTEX", "About", None, QtGui.QApplication.UnicodeUTF8))

