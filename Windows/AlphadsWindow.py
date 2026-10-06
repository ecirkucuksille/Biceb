# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Classes.GeneralComputations import GeneralComputations as gc
import sys

class Alphads_Ui_Form(object):
    def calculate(self):
        alfa_star, alfa_ds = gc.calculate_alfads(int(self.slineEdit.text()), int(self.nlineEdit.text()))
        self.alphastaredit.setText(str(round(alfa_star, 5)))
        self.dsedit.setText(str(round(alfa_ds, 5)))

    def setupUi(self, AlphadsForm):
        AlphadsForm.setObjectName("MainWindow")
        AlphadsForm.resize(414, 76)
        AlphadsForm.setWindowIcon(QtGui.QIcon(sys.path[0] + "/images/biodiversity.ico"))

        self.centralwidget = QtWidgets.QWidget(AlphadsForm)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        self.slabel = QtWidgets.QLabel(self.centralwidget)
        self.slabel.setGeometry(QtCore.QRect(10, 20, 16, 16))
        self.slabel.setFont(font)
        self.slabel.setObjectName("slabel")

        self.slineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.slineEdit.setGeometry(QtCore.QRect(30, 17, 113, 23))
        self.slineEdit.setObjectName("slineEdit")

        self.nlabel = QtWidgets.QLabel(self.centralwidget)
        self.nlabel.setGeometry(QtCore.QRect(10, 50, 16, 16))
        self.nlabel.setFont(font)
        self.nlabel.setObjectName("nlabel")

        self.nlineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nlineEdit.setGeometry(QtCore.QRect(30, 46, 113, 23))
        self.nlineEdit.setObjectName("nlineEdit")

        self.calcButton = QtWidgets.QPushButton(self.centralwidget)
        self.calcButton.setGeometry(QtCore.QRect(155, 31, 80, 23))
        self.calcButton.setFont(font)
        self.calcButton.setObjectName("calcButton")
        self.calcButton.clicked.connect(self.calculate)

        self.alphastarlabel = QtWidgets.QLabel(self.centralwidget)
        self.alphastarlabel.setGeometry(QtCore.QRect(244, 20, 21, 16))
        self.alphastarlabel.setFont(font)
        self.alphastarlabel.setObjectName("alphastarlabel")

        self.alphastaredit = QtWidgets.QLineEdit(self.centralwidget)
        self.alphastaredit.setGeometry(QtCore.QRect(295, 17, 113, 23))
        self.alphastaredit.setObjectName("alphastaredit")

        self.dsedit = QtWidgets.QLineEdit(self.centralwidget)
        self.dsedit.setGeometry(QtCore.QRect(295, 46, 113, 23))
        self.dsedit.setObjectName("dsedit")

        self.dslabel = QtWidgets.QLabel(self.centralwidget)
        self.dslabel.setGeometry(QtCore.QRect(244, 50, 50, 16))
        self.dslabel.setFont(font)
        self.dslabel.setObjectName("dslabel")

        AlphadsForm.setCentralWidget(self.centralwidget)
        self.retranslateUi(AlphadsForm)
        QtCore.QMetaObject.connectSlotsByName(AlphadsForm)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("AlphadsForm", "Alphads Hesaplama Ekranı"))
        self.slabel.setText(_translate("MainWindow", "S"))
        self.nlabel.setText(_translate("MainWindow", "N"))
        self.calcButton.setText(_translate("MainWindow", "Hesapla"))
        self.alphastarlabel.setText(_translate("MainWindow", "α*"))
        self.dslabel.setText(_translate("MainWindow", "α*DMM"))


