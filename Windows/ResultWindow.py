# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResultWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Classes.DataModel import PandasModel
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import platform
from Classes.CustomDelegate import QCustomDelegate
from Classes.GeneralComputations import GeneralComputations as gc

class Ui_ResultWindow(object):

    def copyDataFrame(self):
        self.resultframe.to_clipboard()


    def saveToExcel(self):
        fullfilepath = QtWidgets.QFileDialog.getSaveFileName(None, "Dosya Kaydet","", "Excel files (*.xls *.xlsx)")
        filename = fullfilepath[0] + ".xls"
        self.resultframe.to_excel(filename, engine='xlsxwriter')

    def drawGraphics(self):
        mpl.rcParams['savefig.dpi'] = int(self.DpiComboBox.currentText())
        mpl.rcParams['font.family'] = self.FontComboBox.currentText()
        mpl.rcParams["font.size"] = int(self.FontSizeSpinBox.text())
        mpl.rcParams['lines.linewidth'] = int(self.LineWidthSpinBox.text())
        if self.ostype == 'Linux':
                plt.ion()
        if self.wasopened == 13:
            xvalues = list(self.resultframe)[1:]
            Hvalues = self.resultframe.iloc[0, 1:].values
            Evalues = self.resultframe.iloc[1, 1:].values
            lnEvalues = self.resultframe.iloc[2, 1:].values
            lnEdivlnSvalues = self.resultframe.iloc[3, 1:].values
            #plt.figure().canvas.set_window_title('Grafik')
            plt.figure().canvas.manager.set_window_title('Grafik')
            plt.style.use('grayscale')
            #plt.xlabel('Örnek Alanlar')
            plt.xticks(rotation=90)
            plt.plot(xvalues, Hvalues, linestyle=':', label = 'H')
            plt.plot(xvalues, Evalues, linestyle='-.', label = 'E')
            plt.plot(xvalues, lnEvalues, linestyle='--', label = 'lnE')
            plt.plot(xvalues, lnEdivlnSvalues, linestyle='-', label='lnE/lnS')
            axes = plt.gca()
            axes.yaxis.grid(color='#C0C0C0')
            plt.legend(loc='best')

        if self.wasopened == 17:
            cmpt = gc(self.comeframe)
            grahone, graphtwo = cmpt.calcvarofcomdata(1)
            fig, ax = plt.subplots(2, 1)

            objects = self.comeframe.iloc[:,0].values
            y_pos = np.arange(len(objects))
            ax[0].bar(y_pos, grahone, align='center', alpha=0.5)
            ax[0].set_xticks(y_pos)
            ax[0].set_xticklabels(objects)
            ax[0].set_title('Türlerin Beta Çeşitliliğine Katkı Oranları')


            objectstwo =list(self.comeframe)[1:]
            ytwo_pos = np.arange(len(objectstwo))
            ax[1].bar(ytwo_pos, graphtwo,align='center', alpha=0.5)
            ax[1].set_xticks(ytwo_pos)
            ax[1].set_xticklabels(objectstwo)
            ax[1].set_title('Örnek Alanların Beta Çeşitliliğine Katkı Oranları')

        if self.ostype != 'Linux':
            plt.show()

    def __init__(self,  preparedDataFrame, wasopened=0, comingframe=None):
        self.resultframe = preparedDataFrame
        self.wasopened = wasopened
        self.ostype = platform.system()
        if comingframe is not None:
            self.comeframe = comingframe


    def setupUi(self, ResultWindow):

        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.setWindowIcon(QtGui.QIcon(sys.path[0]+ "/images/biodiversity.ico"))

        #ResultWindow.resize(820, 300)
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 60)


        self.ResultTable = QtWidgets.QTableView(self.centralwidget)
        #self.ResultTable.setGeometry(QtCore.QRect(0, 0, 820, 200))
        self.ResultTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ResultTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ResultTable.verticalHeader().setVisible(False)
        self.ResultTable.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.ResultTable.setStyleSheet("QHeaderView::section { background-color:#F0EEEB }")
        self.ResultTable.setObjectName("ResultTable")

        self.horizontalLayout.addWidget(self.ResultTable)
        self.vlayout.addLayout(self.horizontalLayout)

        ResultWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(ResultWindow)
        self.statusbar.setObjectName("statusbar")
        ResultWindow.setStatusBar(self.statusbar)

        if self.ostype in ['Linux', 'Windows']:
            buttonPosition = int(QtWidgets.QDesktopWidget().screenGeometry().height() * 0.88)
        else:
            buttonPosition = int(QtWidgets.QDesktopWidget().screenGeometry().height() * 0.92)


        # Copy Button Added
        self.CopyButton = QtWidgets.QPushButton(self.centralwidget)
        self.CopyButton.setText("Kopyala")
        self.CopyButton.setGeometry(QtCore.QRect(10,  buttonPosition, 75, 20))
        self.CopyButton.setObjectName("CopyButton")
        self.CopyButton.clicked.connect(self.copyDataFrame)

        QtCore.QRect()

        # Export Excel Button Added
        self.ExcelButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExcelButton.setText("Excel'e Aktar")
        self.ExcelButton.setGeometry(QtCore.QRect(100, buttonPosition, 85, 20))
        self.ExcelButton.setObjectName("ExcelButton")
        self.ExcelButton.clicked.connect(self.saveToExcel)

        # Graphics Button Added
        self.GraphicsButton = QtWidgets.QPushButton(self.centralwidget)
        self.GraphicsButton.setText("Grafik Çiz")
        self.GraphicsButton.setGeometry(QtCore.QRect(200,  buttonPosition, 95, 20))
        self.GraphicsButton.setObjectName("GraphicsButton")
        self.GraphicsButton.clicked.connect(self.drawGraphics)

        #Font Combobox and Font Label Added

        self.FontLabel = QtWidgets.QLabel(self.centralwidget)
        self.FontLabel.setText("Font Seçiniz")
        self.FontLabel.setGeometry(QtCore.QRect(300,  buttonPosition, 105, 20))
        self.FontLabel.setObjectName("FontLabel")

        self.FontComboBox = QtWidgets.QFontComboBox(self.centralwidget)
        self.FontComboBox.setGeometry(QtCore.QRect(380,  buttonPosition, 115, 20))
        self.FontComboBox.setObjectName("FontComboBox")

        #Font Size SpinBox and Font Size Label added
        self.FontSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.FontSizeLabel.setText("Font Büyüklüğü")
        self.FontSizeLabel.setGeometry(QtCore.QRect(500,  buttonPosition, 125, 20))
        self.FontSizeLabel.setObjectName("FontSizeLabel")

        self.FontSizeSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.FontSizeSpinBox.setRange(10, 20)
        self.FontSizeSpinBox.setGeometry(QtCore.QRect(600,  buttonPosition, 135, 20))
        self.FontSizeSpinBox.setMinimum(2)
        self.FontSizeSpinBox.setObjectName("FontSizeSpinBox")

        #Graphic dpi Combobox and Label added
        self.DpiLabel = QtWidgets.QLabel(self.centralwidget)
        self.DpiLabel.setText("Grafik Kalitesi(dpi)")
        self.DpiLabel.setGeometry(QtCore.QRect(740,  buttonPosition, 125, 20))
        self.DpiLabel.setObjectName("DpiLabel")

        self.DpiComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.DpiComboBox.setGeometry(QtCore.QRect(860,  buttonPosition, 135, 20))
        self.DpiComboBox.setObjectName("DpiComboBox")

        self.DpiComboBox.addItem("150")
        self.DpiComboBox.addItem("300")
        self.DpiComboBox.addItem("600")

        #Line width Label and Line width spinbox added
        self.LineWidthLabel = QtWidgets.QLabel(self.centralwidget)
        self.LineWidthLabel.setText("Çizgi Kalınlığı")
        self.LineWidthLabel.setGeometry(QtCore.QRect(1000,  buttonPosition, 125, 20))
        self.LineWidthLabel.setObjectName("LineWidthLabel")

        self.LineWidthSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.LineWidthSpinBox.setRange(2, 5)
        self.LineWidthSpinBox.setGeometry(QtCore.QRect(1100,  buttonPosition, 135, 20))
        self.LineWidthSpinBox.setMinimum(2)

        self.LineWidthSpinBox.setObjectName("LineWidthSpinBox")



        if self.wasopened in [13, 17]:
            self.GraphicsButton.setVisible(True)
            self.FontLabel.setVisible(True)
            self.FontComboBox.setVisible(True)
            self.FontSizeLabel.setVisible(True)
            self.FontSizeSpinBox.setVisible(True)
            self.DpiLabel.setVisible(True)
            self.DpiComboBox.setVisible(True)
            self.LineWidthLabel.setVisible(True)
            self.LineWidthSpinBox.setVisible(True)
        else:
            self.GraphicsButton.setVisible(False)
            self.FontLabel.setVisible(False)
            self.FontComboBox.setVisible(False)
            self.FontSizeLabel.setVisible(False)
            self.FontSizeSpinBox.setVisible(False)
            self.DpiLabel.setVisible(False)
            self.DpiComboBox.setVisible(False)
            self.LineWidthLabel.setVisible(False)
            self.LineWidthSpinBox.setVisible(False)


        # Window move to active screeen center
        fg = ResultWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        ResultWindow.move(fg.topLeft())

        self.retranslateUi(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

        model = PandasModel(self.resultframe)


        self.ResultTable.setModel(model)
        self.ResultTable.setWordWrap(True)
        self.ResultTable.resizeRowsToContents()
        if self.wasopened == 4:
            qdelegate = QCustomDelegate()
            qdelegate.controlcolumn = 3
            self.ResultTable.setItemDelegate(qdelegate)
        elif self.wasopened == 6:
            qdelegate = QCustomDelegate()
            qdelegate.controlcolumn = 2
            self.ResultTable.setItemDelegate(qdelegate)
        else:
            qdelegate = QCustomDelegate()
            self.ResultTable.setItemDelegate(qdelegate)

    def retranslateUi(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "Sonuç Ekranı"))


