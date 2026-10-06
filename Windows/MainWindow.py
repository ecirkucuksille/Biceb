# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtGui
from Classes.DataModel import PandasModel
from Windows.ResultWindow import Ui_ResultWindow
from Windows.AboutWindow import Ui_Form
from Windows.AlphadsWindow import Alphads_Ui_Form
from Windows.BigResultWindow import Ui_BigResultWindow
from Windows.SheetsWindow import Ui_SheetWindow
from Classes.PrepareDataFrame import PrepareDataFrame as pdf
from Classes.DataFrameForBigWindow import DataFrameForBigWindow as dbfw
import pandas as pd
import platform
import sys
import subprocess


class Ui_MainWindow(QtWidgets.QMainWindow):
    # define class global variables
    dataframe = None
    selectedSheet = ""
    ostype = platform.system()
    # define openfile function
    def openfile(self):
        fullfilepath = QtWidgets.QFileDialog.getOpenFileName(None, "Dosya Aç", "",
                                                             "Tüm Dosyalar (*);;csv dosyalar (*.csv);; xls dosyalar (*.xls);; xlsx dosyalar (*.xlsx)")
        # file extension controlled
        if fullfilepath[0] != '':

            dotposition = fullfilepath[0].find('.')
            fileextension = fullfilepath[0][dotposition + 1:]
            if fileextension == "csv":
                self.dataframe = pd.read_csv(fullfilepath[0])
            elif fileextension == "xls" or fileextension == "xlsx":
                excelfile = pd.ExcelFile(fullfilepath[0])
                sheetlist = excelfile.sheet_names
                if len(sheetlist) == 1:
                    self.dataframe = pd.read_excel(fullfilepath[0])
                else:
                    sheetwindow = Ui_SheetWindow(sheetlist, self)
                    sheetwindow.exec_()
                    if self.selectedSheet != '':
                        self.dataframe = excelfile.parse(sheet_name=self.selectedSheet)
                        self.selectedSheet = ""
                    else:
                        QtWidgets.QMessageBox.warning(None, "Hata", "Desteklenmeyen Dosya Formatı Seçtiniz")
            else:
                QtWidgets.QMessageBox.information(None, "Bilgi", "Bir Çalışma Dosyası Seçmediniz")

            if fullfilepath[0] != '' and self.dataframe is not None:
                self.RowLabel.setText("Satır Sayısı : " + str(self.dataframe.shape[0]))
                self.ColLabel.setText("Sütun Sayısı : " + str(self.dataframe.shape[1]))
                # model_df = self.dataframe.iloc[0:24, 0:10]
                model = PandasModel(self.dataframe)
                self.DataList.setModel(model)
                col_sums = self.dataframe.sum()
                zero_values = col_sums[col_sums==0]
                if len(zero_values) != 0:
                    QtWidgets.QMessageBox.warning(None, "Bilgi",
                                                  f"{zero_values.index.str.cat(sep=',')} alanları tür içermiyor.\n"
                                                  "Lütfen hesaplamalardan önce modelden çıkarınız")

    # The function that calling the resultwindow for the speciesrichness has been defined
    def calculatespeciesrichenss(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 1)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 1 for specify richness
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the Margalef & Menhinick has been defined
    def calculatemargamenh(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 2, self.progressbar)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 2 for Margalef & Menhinick
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the Chao1 has been defined
    def calculatechao(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 3)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 3 for Chao1
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the bigresultwindow for the dependent rarefaction has been defined
    def calculatedependent(self):
        createdDataFrame = dbfw.createDataFrame(self.dataframe, 1, self.progressbar)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_BigResultWindow(createdDataFrame, 1)  # 1 for dependent
        self.ui.setupUi(self.window)
        self.window.showMaximized()
        self.progressbar.setValue(0)

    # The function that calling the bigresultwindow for the independent rarefaction has been defined
    def calculateindependent(self):
        #bigframe = dbfw(self.dataframe, 2)
        createdDataFrame = dbfw.createDataFrame(self.dataframe, 2, self.progressbar)
        #createdDataFrame = bigframe.createDataFrame()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_BigResultWindow(createdDataFrame, 2)  # 2 for independent
        self.ui.setupUi(self.window)
        if self.ostype in ['Windows', 'Linux']:
            self.window.showMaximized()
        else:
            self.window.showFullScreen()
        self.progressbar.setValue(0)

    # The function that calling the alphadswindow for the calculate alphads
    def calcalphads(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.window = QtWidgets.QMainWindow()
        self.ui = Alphads_Ui_Form()
        self.ui.setupUi(self.window)
        self.window.move(qtRectangle.topLeft())
        self.window.show()

    # The function that calling the resultwindow for the shannonwiener index has been defined
    def calculateshannonwiener(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 4)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame, 4)  # 4 for Shannon-Wiener
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the brillouin index has been defined
    def calculatebrillouin(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 5)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 5 for brillouin
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the simpson index has been defined
    def calculatesimpson(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 6)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame, 6)  # 6 for simpson
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the mcintosh index has been defined
    def calculatemcintosh(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 7)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 7 for mcintosh
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the berger-parker index has been defined
    def calculatebergerparker(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 8)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 8 for berger-parker
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the qstatistics has been defined
    def calculateqstatistic(self):
        self.window = QtWidgets.QMainWindow()
        createdDataFrame = pdf.createDataFrame(self.dataframe, 9)
        self.ui = Ui_ResultWindow(createdDataFrame)  # 9 for qstatistics
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the logseries has been defined
    def calculatelogseries(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 10)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 10 for logseries
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the lognormal has been defined
    def calculatelognormal(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 11)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 11 for lognormal
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the jackknifing has been defined
    def calculatejackknifing(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 12)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 12 for jackknifing
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for the sheanalysis has been defined
    def calculatesheanalysis(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 13)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame, 13)  # 13 for sheanalysis
        self.ui.setupUi(self.window)
        if self.ostype in ['Windows', 'Linux']:
            self.window.showMaximized()
        else:
            self.window.showFullScreen()

    # The function that calling the resultwindow for the yesno two comunity beta
    def calculatetwocomunity(self):
        df = self.dataframe.copy()
        for x in df.columns:
            df[x] = df[x].map(lambda item: 1 if type(item) == int and item > 0 else item)

        # get selected columns
        selectedindex = self.DataList.selectedIndexes()
        selcollist = []
        for val in selectedindex:
            try:
                idx = selcollist.index(val.column())
            except ValueError:
                selcollist.append(val.column())
        if len(selcollist) == 2 or len(selcollist) == 0:
            createdDataFrame = pdf.createDataFrame(df, 14, selcollist)
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ResultWindow(createdDataFrame)  # 14 for two comunity
            self.ui.setupUi(self.window)
            self.window.showMaximized()
        else:
            QtWidgets.QMessageBox.warning(None, "Hata", "İkiden fazla sütun seçemezsiniz")

    # The function that calling the resultwindow for the countable two comunity
    def calculatecnttwocomunity(self):
        # get selected columns
        selectedindex = self.DataList.selectedIndexes()
        selcollist = []
        for val in selectedindex:
            try:
                idx = selcollist.index(val.column())
            except ValueError:
                selcollist.append(val.column())
        if len(selcollist) == 2 or len(selcollist) == 0:
            createdDataFrame = pdf.createDataFrame(self.dataframe, 15, selcollist)
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ResultWindow(createdDataFrame)  # 15 for countable two comunity
            self.ui.setupUi(self.window)
            self.window.showMaximized()
        else:
            QtWidgets.QMessageBox.warning(None, "Hata", "İkiden fazla sütun seçemezsiniz")

    # The function that calling the resultwindow for the yesno universal beta
    def calculateuniversal(self):
        df = self.dataframe.copy()
        for x in df.columns:
            df[x] = df[x].map(lambda item: 1 if type(item) == int and item > 0 else item)
        createdDataFrame = pdf.createDataFrame(df, 16)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 16 for yesno universal
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for Variance of Community Data
    def calculatevarofcomdata(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 17)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame, 17, self.dataframe)  # 17 for Variance of Community Data
        self.ui.setupUi(self.window)
        if self.ostype in ['Windows', 'Linux']:
            self.window.showMaximized()
        else:
            self.window.showFullScreen()

    # The function that calling the resultwindow for simpson beta
    def calculatesimpsonbeta(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 18)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 18 for simpson beta
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for shannon beta
    def calculateshannonbeta(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 19)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 19 for shannon beta
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    # The function that calling the resultwindow for shannon beta exponential
    def calculateshannonbetaexp(self):
        createdDataFrame = pdf.createDataFrame(self.dataframe, 20)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultWindow(createdDataFrame)  # 20 for shannon beta exponential
        self.ui.setupUi(self.window)
        self.window.showMaximized()

    def showabout(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.move(qtRectangle.topLeft())
        self.window.show()

    def showcontextmenu(self, QContextMenuEvent):
        self.menu = QtWidgets.QMenu(self.DataList)
        # adding removecolumnaction
        removeAction = QtWidgets.QAction('Sütun Sil', self.DataList)
        self.menu.addAction(removeAction)
        removeAction.triggered.connect(self.removecol)

        # adding addcolumnaction
        addColAction = QtWidgets.QAction('Sütun Ekle', self.DataList)
        self.menu.addAction(addColAction)
        addColAction.triggered.connect(self.addcol)

        # adding addrowaction
        addRowAction = QtWidgets.QAction('Satır Ekle', self.DataList)
        self.menu.addAction(addRowAction)
        addRowAction.triggered.connect(self.addrow)
        '''
        #adding removerowaction
        removeRowAction = QtWidgets.QAction('Satır Sil', self.DataList)
        self.menu.addAction(removeRowAction)
        removeRowAction.triggered.connect(self.removerow)
        '''
        self.menu.popup(QtGui.QCursor.pos())

    def addcol(self):
        text, ok = QtWidgets.QInputDialog.getText(None, 'Örnek Alan İsmini Giriniz', 'Örnek Alan ismi:')
        if ok:
            self.dataframe[text] = 0
            model = PandasModel(self.dataframe)
            self.DataList.setModel(model)

    def removecol(self):
        # Determining selected columns
        selectedindex = self.DataList.selectedIndexes()
        selcollist = []
        for val in selectedindex:
            try:
                idx = selcollist.index(val.column())
            except ValueError:
                selcollist.append(val.column())

        self.dataframe.drop(self.dataframe.columns[selcollist], axis=1, inplace=True)
        model = PandasModel(self.dataframe)
        self.DataList.setModel(model)

    def addrow(self):
        text, ok = QtWidgets.QInputDialog.getText(None, 'Tür İsmini Giriniz', 'Tür ismi:')
        if ok:
            rowList = [text]
            for i in range(0, self.dataframe.shape[1] - 1):
                rowList.append(0)
            newRow = pd.Series(rowList, self.dataframe.columns)
            self.dataframe = self.dataframe.append(newRow, ignore_index=True)
            model = PandasModel(self.dataframe)
            self.DataList.setModel(model)

    def removerow(self):
        selection = self.DataList.selectionModel().selectedRows()
        selrowlist = []
        for val in selection:
            selrowlist.append(val.row())
        print(selrowlist)

    def closeproject(self):
        sys.exit()

    def showuserguide(self):
        if self.ostype == 'Windows':
            file_path = sys.path[0] + '\\userguide.pdf'
            subprocess.call(['explorer.exe',file_path])
        else:
            file_path = sys.path[0] + '/userguide.pdf'
            subprocess.call(['xdg-open',file_path])

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(sys.path[0] + "/images/biodiversity.ico"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 12, 0, 0)

        self.DataList = QtWidgets.QTableView(self.centralwidget)
        # self.DataList.setGeometry(QtCore.QRect(0, 20, 811, 571))
        self.DataList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.DataList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.DataList.verticalHeader().setVisible(False)
        self.DataList.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.DataList.setStyleSheet("QHeaderView::section { background-color:#F0EEEB }")
        self.DataList.setObjectName("DataList")

        self.DataList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.DataList.customContextMenuRequested.connect(self.showcontextmenu)

        self.horizontalLayout.addWidget(self.DataList)
        self.vlayout.addLayout(self.horizontalLayout)

        font = QtGui.QFont()
        font.setBold(True)

        self.RowLabel = QtWidgets.QLabel(self.centralwidget)
        self.RowLabel.setText("Satır Sayısı : 0")
        self.RowLabel.setGeometry(QtCore.QRect(10, 5, 115, 16))
        self.RowLabel.setFont(font)
        self.RowLabel.setObjectName("RowLabel")

        self.ColLabel = QtWidgets.QLabel(self.centralwidget)
        self.ColLabel.setText("Sütun Sayısı : 0")
        self.ColLabel.setGeometry(QtCore.QRect(135, 5, 117, 16))
        self.ColLabel.setFont(font)
        self.ColLabel.setObjectName("ColLabel")

        MainWindow.setCentralWidget(self.centralwidget)

        # Window move to active screeen center
        fg = MainWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        MainWindow.move(fg.topLeft())

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")

        self.menubar.setNativeMenuBar(False)

        self.menuDosya = QtWidgets.QMenu(self.menubar)
        self.menuDosya.setObjectName("menuDosya")

        self.menucesitlilik = QtWidgets.QMenu(self.menubar)
        self.menucesitlilik.setObjectName("menucesitlilik")

        self.Rarefaction = QtWidgets.QMenu(self.menucesitlilik)
        self.Rarefaction.setObjectName("Rarefaction")

        self.numorrateindices = QtWidgets.QMenu(self.menubar)
        self.numorrateindices.setObjectName("menunumrateind")

        self.specabundmodel = QtWidgets.QMenu(self.menubar)
        self.specabundmodel.setObjectName("specabundmodel")

        self.betadiversity = QtWidgets.QMenu(self.menubar)
        self.betadiversity.setObjectName("betadiversity")

        self.yesno = QtWidgets.QMenu(self.menubar)
        self.yesno.setObjectName("yesno")

        self.countable = QtWidgets.QMenu(self.menubar)
        self.countable.setObjectName("countable")

        self.menuYardim = QtWidgets.QMenu(self.menubar)
        self.menuYardim.setObjectName("menuYardim")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        # menu items for file
        self.OpenFile = QtWidgets.QAction(MainWindow)
        self.OpenFile.setObjectName("OpenFile")
        self.OpenFile.triggered.connect(self.openfile)

        '''
        self.SaveFile = QtWidgets.QAction(MainWindow)
        self.SaveFile.setObjectName("SaveFile")

        self.SaveAsFile = QtWidgets.QAction(MainWindow)
        self.SaveAsFile.setObjectName("SaveAsFile")
        '''
        self.CloseProject = QtWidgets.QAction(MainWindow)
        self.CloseProject.setObjectName("CloseProject")
        self.CloseProject.triggered.connect(self.closeproject)

        # menu items for species
        self.SpeciesRichness = QtWidgets.QAction(MainWindow)
        self.SpeciesRichness.setObjectName("SpeciesRichness")
        self.SpeciesRichness.triggered.connect(self.calculatespeciesrichenss)

        self.MargaMenh = QtWidgets.QAction(MainWindow)
        self.MargaMenh.setObjectName("MargaMenh")
        self.MargaMenh.triggered.connect(self.calculatemargamenh)

        self.Chao = QtWidgets.QAction(MainWindow)
        self.Chao.setObjectName("Chao")
        self.Chao.triggered.connect(self.calculatechao)

        self.actionDependent = QtWidgets.QAction(MainWindow)
        self.actionDependent.setObjectName("actionDependent")
        self.actionDependent.triggered.connect(self.calculatedependent)

        self.actionIndependent = QtWidgets.QAction(MainWindow)
        self.actionIndependent.setObjectName("actionIndependent")
        self.actionIndependent.triggered.connect(self.calculateindependent)

        self.actionAlphads = QtWidgets.QAction(MainWindow)
        self.actionAlphads.setObjectName("actionAlphads")
        self.actionAlphads.triggered.connect(self.calcalphads)


        # menu items for number or rate indices
        self.shannonWiener = QtWidgets.QAction(MainWindow)
        self.shannonWiener.setObjectName("shannonWiener")
        self.shannonWiener.triggered.connect(self.calculateshannonwiener)

        self.brillouin = QtWidgets.QAction(MainWindow)
        self.brillouin.setObjectName("shannonWiener")
        self.brillouin.triggered.connect(self.calculatebrillouin)

        self.simpson = QtWidgets.QAction(MainWindow)
        self.simpson.setObjectName("simpson")
        self.simpson.triggered.connect(self.calculatesimpson)

        self.mcintosh = QtWidgets.QAction(MainWindow)
        self.mcintosh.setObjectName("mcintosh")
        self.mcintosh.triggered.connect(self.calculatemcintosh)

        self.bergerparker = QtWidgets.QAction(MainWindow)
        self.bergerparker.setObjectName("bergerparker")
        self.bergerparker.triggered.connect(self.calculatebergerparker)

        # menu items for species abundance models
        self.qstatistics = QtWidgets.QAction(MainWindow)
        self.qstatistics.setObjectName("qstatistics")
        self.qstatistics.triggered.connect(self.calculateqstatistic)

        self.logseries = QtWidgets.QAction(MainWindow)
        self.logseries.setObjectName("logseries")
        self.logseries.triggered.connect(self.calculatelogseries)

        self.lognormal = QtWidgets.QAction(MainWindow)
        self.lognormal.setObjectName("lognormal")
        self.lognormal.triggered.connect(self.calculatelognormal)

        self.jackknifing = QtWidgets.QAction(MainWindow)
        self.jackknifing.setObjectName("jackknifing")
        self.jackknifing.triggered.connect(self.calculatejackknifing)

        self.sheanalysis = QtWidgets.QAction(MainWindow)
        self.sheanalysis.setObjectName("sheanalysis")
        self.sheanalysis.triggered.connect(self.calculatesheanalysis)

        # menu items for betadiversity

        self.twocomunity = QtWidgets.QAction(MainWindow)
        self.twocomunity.setObjectName("twocomunity")
        self.twocomunity.triggered.connect(self.calculatetwocomunity)

        self.universal = QtWidgets.QAction(MainWindow)
        self.universal.setObjectName("universal")
        self.universal.triggered.connect(self.calculateuniversal)

        self.cnttwocomunity = QtWidgets.QAction(MainWindow)
        self.cnttwocomunity.setObjectName("cnttwocomunity")
        self.cnttwocomunity.triggered.connect(self.calculatecnttwocomunity)

        self.varofcomdata = QtWidgets.QAction(MainWindow)
        self.varofcomdata.setObjectName("varofcomdata")
        self.varofcomdata.triggered.connect(self.calculatevarofcomdata)

        self.simpsonbeta = QtWidgets.QAction(MainWindow)
        self.simpsonbeta.setObjectName("simpsonbeta")
        self.simpsonbeta.triggered.connect(self.calculatesimpsonbeta)

        self.shannonbeta = QtWidgets.QAction(MainWindow)
        self.shannonbeta.setObjectName("shannonbeta")
        self.shannonbeta.triggered.connect(self.calculateshannonbeta)

        self.shannonbetaexp = QtWidgets.QAction(MainWindow)
        self.shannonbetaexp.setObjectName("shannonbetaexp")
        self.shannonbetaexp.triggered.connect(self.calculateshannonbetaexp)

        # menu items for help
        self.AboutProgram = QtWidgets.QAction(MainWindow)
        self.AboutProgram.setObjectName("AboutProgram")
        self.AboutProgram.triggered.connect(self.showabout)

        #menu items for user guide
        self.userguide = QtWidgets.QAction(MainWindow)
        self.userguide.setObjectName("userguide")
        self.userguide.triggered.connect(self.showuserguide)



        self.menuDosya.addAction(self.OpenFile)
        # self.menuDosya.addAction(self.SaveFile)
        # self.menuDosya.addAction(self.SaveAsFile)
        self.menuDosya.addAction(self.CloseProject)

        self.menucesitlilik.addAction(self.SpeciesRichness)
        self.menucesitlilik.addAction(self.MargaMenh)
        self.menucesitlilik.addAction(self.Chao)
        self.Rarefaction.addAction(self.actionDependent)
        self.Rarefaction.addAction(self.actionIndependent)
        self.menucesitlilik.addAction(self.Rarefaction.menuAction())
        self.menucesitlilik.addAction(self.actionAlphads)

        self.numorrateindices.addAction(self.shannonWiener)
        self.numorrateindices.addAction(self.brillouin)
        self.numorrateindices.addAction(self.simpson)
        self.numorrateindices.addAction(self.mcintosh)
        self.numorrateindices.addAction(self.bergerparker)

        self.specabundmodel.addAction(self.qstatistics)
        self.specabundmodel.addAction(self.logseries)
        self.specabundmodel.addAction(self.lognormal)
        self.specabundmodel.addAction(self.jackknifing)
        self.specabundmodel.addAction(self.sheanalysis)

        self.yesno.addAction(self.twocomunity)
        self.yesno.addAction(self.universal)
        self.betadiversity.addAction(self.yesno.menuAction())
        self.countable.addAction(self.cnttwocomunity)
        self.countable.addAction(self.varofcomdata)
        self.countable.addAction(self.simpsonbeta)
        self.countable.addAction(self.shannonbeta)
        self.countable.addAction(self.shannonbetaexp)
        self.betadiversity.addAction(self.countable.menuAction())

        self.menuYardim.addAction(self.AboutProgram)
        self.menuYardim.addAction(self.userguide)

        self.menubar.addAction(self.menuDosya.menuAction())
        self.menubar.addAction(self.menucesitlilik.menuAction())
        self.menubar.addAction(self.numorrateindices.menuAction())
        self.menubar.addAction(self.specabundmodel.menuAction())
        self.menubar.addAction(self.betadiversity.menuAction())
        self.menubar.addAction(self.menuYardim.menuAction())


        self.progressbar = QtWidgets.QProgressBar(self)
        #self.progressbar.setGeometry(10, 5, 115, 20)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(400)
        self.progressbar.setValue(0)
        self.progressbar.setFixedWidth(400)
        self.progressbar.setObjectName("progressbar")
        self.statusbar.addPermanentWidget(self.progressbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Biyolojik Çeşitlilik Bileşen Hesaplama Yazılımı"))
        self.menuDosya.setTitle(_translate("MainWindow", "Dosya"))
        self.OpenFile.setText(_translate("MainWindow", "Aç"))
        # self.SaveFile.setText(_translate("MainWindow", "Kaydet"))
        # self.SaveAsFile.setText(_translate("MainWindow", "Farklı Kaydet"))
        self.CloseProject.setText(_translate("MainWindow", "Kapat"))

        self.menucesitlilik.setTitle(_translate("MainWindow", "Çeşitlilik"))
        self.SpeciesRichness.setText(_translate("MainWindow", "Tür Zenginliği"))
        self.MargaMenh.setText(_translate("MainWindow", "DMG, DMN && DMM"))
        self.Chao.setText(_translate("MainWindow", "Chao1"))
        self.Rarefaction.setTitle(_translate("MainWindow", "Seyreltme"))
        self.actionDependent.setText(_translate("MainWindow", "Bağımlı"))
        self.actionIndependent.setText(_translate("MainWindow", "Bağımsız"))
        self.actionAlphads.setText(_translate("MainWindow", "DMM"))

        self.numorrateindices.setTitle(_translate("MainWindow", "Say.Or.İndisler"))
        self.shannonWiener.setText(_translate("MainWindow", "Shannon-Wiener"))
        self.brillouin.setText(_translate("MainWindow", "Brillouin"))
        self.simpson.setText(_translate("MainWindow", "Simpson"))
        self.mcintosh.setText(_translate("MainWindow", "McIntosh"))
        self.bergerparker.setText(_translate("MainWindow", "Berger-Parker"))

        self.specabundmodel.setTitle(_translate("MainWindow", "Tür Bolluk"))
        self.qstatistics.setText(_translate("MainWindow", "Q İstatistiği"))
        self.logseries.setText(_translate("MainWindow", "Log Serileri"))
        self.lognormal.setText(_translate("MainWindow", "Log Normal"))
        self.jackknifing.setText(_translate("MainWindow", "Jack Knifing"))
        self.sheanalysis.setText(_translate("MainWindow", "SHE Analizi"))

        self.betadiversity.setTitle(_translate("MainWindow", "Beta Çeşitliliği"))
        self.yesno.setTitle(_translate("MainWindow", "Var Yok Verileri"))
        self.twocomunity.setText(_translate("MainWindow", "İki Toplumlu"))
        self.universal.setText(_translate("MainWindow", "Evrensel"))
        self.countable.setTitle(_translate("MainWindow", "Sayılabilen Veriler"))
        self.cnttwocomunity.setText(_translate("MainWindow", "İki Toplumlu"))
        self.varofcomdata.setText(_translate("MainWindow", "Toplum Ver. Varyansı"))
        self.simpsonbeta.setText(_translate("MainWindow", "Simpson"))
        self.shannonbeta.setText(_translate("MainWindow", "Shannon"))
        self.shannonbetaexp.setText(_translate("MainWindow", "Shannon Üssel"))

        self.menuYardim.setTitle(_translate("MainWindow", "Yardım"))
        self.AboutProgram.setText(_translate("MainWindow", "Hakkında"))
        self.userguide.setText(_translate("MainWindow", "Kullanım Kılavuzu"))
