# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SheetsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_SheetWindow(QtWidgets.QDialog):
    sheetlists = []
    parentobject = None
    def __init__(self, sheetlist, comingobject):
        QtWidgets.QDialog.__init__(self)
        self.sheetlists = sheetlist
        self.parentobject = comingobject
        self.setupUi(self)
        self.setModal(True)



    def selecttext(self):
        self.parentobject.selectedSheet = str(self.sheetCombobox.currentText())
        self.close()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon(sys.path[0]+ "/images/biodiversity.ico"))

        Form.resize(480, 120)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 451, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 361, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sheetCombobox = QtWidgets.QComboBox(Form)
        self.sheetCombobox.setGeometry(QtCore.QRect(150, 50, 141, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sheetCombobox.setFont(font)
        self.sheetCombobox.setObjectName("sheetCombobox")
        self.selecButton = QtWidgets.QPushButton(Form)
        self.selecButton.setGeometry(QtCore.QRect(180, 80, 80, 23))
        self.selecButton.clicked.connect(self.selecttext)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.selecButton.setFont(font)
        self.selecButton.setObjectName("selecButton")

        for elm in self.sheetlists:
            self.sheetCombobox.addItem(elm)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Çalışma Sayfası Listesi"))
        self.label.setText(_translate("Form", "Seçtiğiniz Excel dokümanında birden fazla çalışma sayfası mevcut"))
        self.label_2.setText(_translate("Form", "Lütfen çalışmak istediğiniz çalışma sayfasını seçiniz"))
        self.selecButton.setText(_translate("Form", "Seç"))

