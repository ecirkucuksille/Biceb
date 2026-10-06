# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import sys

class Ui_Form(object):
    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))

    def setupUi(self, AboutForm):
        AboutForm.setObjectName("AboutForm")
        AboutForm.setWindowIcon(QtGui.QIcon(sys.path[0]+ "/images/biodiversity.ico"))

        AboutForm.resize(370, 400)

        self.centralwidget = QtWidgets.QWidget(AboutForm)
        self.centralwidget.setObjectName("centralwidget")


        self.imagelabel = QtWidgets.QLabel(AboutForm)
        self.imagelabel.setGeometry(QtCore.QRect(10, 5, 771, 340))
        self.imagelabel.setText("")
        self.imagelabel.setPixmap(QtGui.QPixmap(sys.path[0]+ "/images/images.png"))
        self.imagelabel.setObjectName("imagelabel")
        self.linklabel = QtWidgets.QLabel(AboutForm)
        self.linklabel.setGeometry(QtCore.QRect(90, 350, 230, 20))
        self.linklabel.linkActivated.connect(self.link)
        self.linklabel.setObjectName("linklabel")
        self.connectlabel = QtWidgets.QLabel(AboutForm)
        self.connectlabel.setGeometry(QtCore.QRect(90, 370, 230, 20))
        self.connectlabel.linkActivated.connect(self.link)
        self.connectlabel.setObjectName("connectlabel")


        AboutForm.setCentralWidget(self.centralwidget)
        self.retranslateUi(AboutForm)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("AboutForm", "Hakkında"))
        self.linklabel.setText(_translate("AboutForm", "<a href=\"http://www.kantitatifekoloji.net/biceb\" target=\"_blank\">http://www.kantitatifekoloji.net/biceb </a>"))
        self.connectlabel.setText(_translate("AboutForm", "<a href=\"mailto:bicebdestek@gmail.com\" target=\"_blank\">İletişim : bicebdestek@gmail.com</a>"))


