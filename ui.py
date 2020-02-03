# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Project.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(635, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cbb_screen = QComboBox(self.centralwidget)
        self.cbb_screen.setObjectName(u"cbb_screen")
        self.cbb_screen.setGeometry(QRect(20, 10, 161, 51))
        self.cbb_screen.setMaximumSize(QSize(16777215, 51))
        self.btn_detect_sreen = QPushButton(self.centralwidget)
        self.btn_detect_sreen.setObjectName(u"btn_detect_sreen")
        self.btn_detect_sreen.setGeometry(QRect(30, 70, 141, 51))
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(20, 150, 171, 151))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 10, 81, 31))
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 40, 121, 31))
        self.Speed_Slider = QSlider(self.frame_2)
        self.Speed_Slider.setObjectName(u"Speed_Slider")
        self.Speed_Slider.setGeometry(QRect(10, 80, 151, 22))
        self.Speed_Slider.setOrientation(Qt.Horizontal)
        self.label_speed = QLabel(self.frame_2)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setGeometry(QRect(60, 120, 60, 16))
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(20, 320, 171, 91))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 10, 81, 31))
        self.checkBox_1 = QCheckBox(self.frame_4)
        self.checkBox_1.setObjectName(u"checkBox_1")
        self.checkBox_1.setGeometry(QRect(10, 50, 61, 20))
        self.checkBox_2 = QCheckBox(self.frame_4)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(60, 50, 61, 20))
        self.checkBox_3 = QCheckBox(self.frame_4)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(110, 50, 61, 20))
        self.btn_qrcode = QPushButton(self.centralwidget)
        self.btn_qrcode.setObjectName(u"btn_qrcode")
        self.btn_qrcode.setGeometry(QRect(30, 440, 141, 61))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 520, 121, 21))
        self.label.setStyleSheet(u"")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(200, 10, 421, 541))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 70, 401, 461))
        self.btn_close = QPushButton(self.frame)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setGeometry(QRect(260, 10, 131, 51))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 635, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u767e\u842c\u5f48\u5e55", None))
        self.btn_detect_sreen.setText(QCoreApplication.translate("MainWindow", u"\u5075\u6e2c\u986f\u793a\u5668", None))
#if QT_CONFIG(whatsthis)
        self.label_2.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">\u5f48\u5e55\u901f\u5ea6</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u5feb&lt;---------&gt;\u6162</p></body></html>", None))
        self.label_speed.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">\u5b57\u9ad4\u5927\u5c0f</span></p></body></html>", None))
        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"\u5927", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u4e2d", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u5c0f", None))
        self.btn_qrcode.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a QRCode", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u7576\u524d\u72c0\u614b\uff1a<span style=\" color:#fc0107;\">\u5df2\u9023\u63a5</span></p></body></html>", None))
        self.btn_close.setText(QCoreApplication.translate("MainWindow", u"\u95dc\u9589\u7a0b\u5f0f", None))
    # retranslateUi

