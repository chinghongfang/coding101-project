# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qrcode.ui',
# licensing of 'Qrcode.ui' applies.
#
# Created: Mon Dec 23 23:04:45 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(467, 360)
        self.label_QRcode = QtWidgets.QLabel(Dialog)
        self.label_QRcode.setGeometry(QtCore.QRect(10, 10, 301, 281))
        self.label_QRcode.setText("")
        self.label_QRcode.setObjectName("label_QRcode")
        self.label_http = QtWidgets.QLabel(Dialog)
        self.label_http.setGeometry(QtCore.QRect(10, 310, 441, 31))
        self.label_http.setText("")
        self.label_http.setObjectName("label_http")
        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_ok.setGeometry(QtCore.QRect(330, 40, 111, 61))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_copy = QtWidgets.QPushButton(Dialog)
        self.btn_copy.setGeometry(QtCore.QRect(330, 110, 111, 71))
        self.btn_copy.setObjectName("btn_copy")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.btn_ok.setText(QtWidgets.QApplication.translate("Dialog", "Close", None, -1))
        self.btn_copy.setText(QtWidgets.QApplication.translate("Dialog", "Copy the link", None, -1))

