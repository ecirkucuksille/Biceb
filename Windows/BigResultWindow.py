
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import random
import platform
from Classes.DataModel import PandasModel
from Classes.CheckComboBox import QCheckComboBox

class Ui_BigResultWindow(object):

    def __init__(self, incomeDataFrame, wasOpened=0):
        self.resultframe = incomeDataFrame
        self.wasOpened = wasOpened
        self.ostype = platform.system()

    def copyDataFrame(self):
        self.resultframe.to_clipboard()

    def saveToExcel(self):
        fullfilepath = QtWidgets.QFileDialog.getSaveFileName(None, "Dosya Kaydet","", "Excel files (*.xls *.xlsx)")
        filename = fullfilepath[0] + ".xls"
        self.resultframe.to_excel(filename, engine='xlsxwriter')

    def drawGraphic(self):
        mpl.rcParams['savefig.dpi'] = int(self.DpiComboBox.currentText())
        mpl.rcParams['font.family'] = self.FontComboBox.currentText()
        mpl.rcParams["font.size"] = self.FontSizeSpinBox.text()

        selectedindices = self.FieldsCombobox.checkedIndex()
        if len(selectedindices) == 1 and self.FieldsCombobox.getValueFromIndex(selectedindices[0]) == 'Hepsi':
            selectedindices.clear()
            allindices = self.FieldsCombobox.getAllIndices()
            for ix in allindices:
                selectedindices.append(ix)
        elif len(selectedindices) == 0:
            QtWidgets.QMessageBox.warning(None, "Hata", "Önce Bir Örnek Alan Seçmelisiniz")
            return
        elif len(selectedindices) > 1:
            for ix in selectedindices:
                if self.FieldsCombobox.getValueFromIndex(ix) == 'Hepsi':
                    QtWidgets.QMessageBox.warning(None, "Hata", "Hem Örnek Alan Hem de Hepsi Seçenekleri Beraber Seçilemez")
                    return


        for selectedindex in selectedindices:
            realindex = 2 * selectedindex + 1
            #print(self.resultframe.iloc[:, realindex].values)
            drawxvalues = []
            drawyvalues = []
            sdvalues = []
            row_number = 0
            for x in self.resultframe.iloc[:, realindex].values:
                if x > 0:
                    drawyvalues.append(x)
                    drawxvalues.append(self.resultframe.iloc[row_number, 0])
                    sdvalues.append(self.resultframe.iloc[row_number, realindex + 1])
                row_number += 1
            #drawyvalues = [x for x in self.resultframe.iloc[:, realindex].values if x > 0]
            #drawxvalues =self.resultframe.iloc[0:len(drawyvalues), 0].values
            if  not self.GraphicTypeCheckBox.isChecked():
                uppervalues = [drawyvalues[i] + sdvalues[i] for i in range(len(drawyvalues))]
                lowervalues = [drawyvalues[i] - sdvalues[i] for i in range(len(drawyvalues))]
            if self.ostype == 'Linux':
                plt.ion()
            #plt.figure().canvas.set_window_title('Grafik')
            #plt.style.use('grayscale')

            #plt.ylabel('E(' + self.FieldsCombobox.currentText() + ') (%95 Güven Aralığı)' )
            linecolor = (random.random(), random.random(), random.random())
            plt.plot(drawxvalues, drawyvalues, linestyle=':', linewidth=1, color=linecolor, label=self.FieldsCombobox.getValueFromIndex(selectedindex))
            if  not self.GraphicTypeCheckBox.isChecked():
                plt.plot(drawxvalues, uppervalues, linestyle='-.', linewidth=1, color=linecolor, label=self.FieldsCombobox.getValueFromIndex(selectedindex))
                plt.plot(drawxvalues, lowervalues, linestyle='--', linewidth=1, color=linecolor)
        '''
        plt.annotate(self.FieldsCombobox.currentText(),
                     (drawxvalues[len(drawxvalues)-1], drawyvalues[len(drawyvalues)-1]),
                     textcoords='offset points',
                     xytext=(0,10),
                     ha='center')
        
        plt.fill_between(drawxvalues, lowervalues, uppervalues, color=(random.random(),
                                                                       random.random(),
                                                                        random.random()), alpha=0.5)
        '''
        plt.xlabel('n')
        plt.ylabel('(E(s) %95 Güven Aralığı)')
        plt.legend()
        if self.ostype != 'Linux':
            plt.show()

    def setupUi(self, BigResultWindow):
        # begin process
        #model_df = self.resultframe.iloc[0:24, 0:10]
        model = PandasModel(self.resultframe)


        BigResultWindow.setObjectName("BigResultWindow")
        BigResultWindow.setWindowIcon(QtGui.QIcon(sys.path[0]+ "/images/biodiversity.ico"))

        #BigResultWindow.resize(820, 300)
        self.centralwidget = QtWidgets.QWidget(BigResultWindow)
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

        BigResultWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(BigResultWindow)
        self.statusbar.setObjectName("statusbar")
        BigResultWindow.setStatusBar(self.statusbar)

        # Information Label added
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(8)

        if self.ostype in ['Linux', 'Windows']:
            buttonPosition = int(QtWidgets.QDesktopWidget().screenGeometry().height() * 0.86)
        else:
            buttonPosition = int(QtWidgets.QDesktopWidget().screenGeometry().height() * 0.92)

        # Copy Button Added
        self.CopyButton = QtWidgets.QPushButton(self.centralwidget)
        self.CopyButton.setText("Kopyala")
        self.CopyButton.setGeometry(QtCore.QRect(10, buttonPosition, 75, 20))
        self.CopyButton.setObjectName("CopyButton")
        self.CopyButton.clicked.connect(self.copyDataFrame)
        # Export Excel Button Added

        self.ExcelButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExcelButton.setText("Excel'e Aktar")
        self.ExcelButton.setGeometry(QtCore.QRect(100, buttonPosition, 85, 20))
        self.ExcelButton.setObjectName("ExcelButton")
        self.ExcelButton.clicked.connect(self.saveToExcel)

        # FieldsLabel added
        self.FieldsLabel = QtWidgets.QLabel(self.centralwidget)
        self.FieldsLabel.setText("Örnek Alan Seçiniz")
        self.FieldsLabel.setGeometry(QtCore.QRect(200, buttonPosition, 120, 20))
        self.FieldsLabel.setFont(font)
        self.FieldsLabel.setObjectName("FieldsLabel")

        # Fields combobox added
        self.FieldsCombobox = QCheckComboBox(self.centralwidget)
        self.FieldsCombobox.setGeometry(QtCore.QRect(320, buttonPosition, 100, 20))
        self.FieldsCombobox.setObjectName(("FieldsCombobox"))

        #Font Combobox and Font Label Added
        self.FontLabel = QtWidgets.QLabel(self.centralwidget)
        self.FontLabel.setText("Font Seçiniz")
        self.FontLabel.setGeometry(QtCore.QRect(430,  buttonPosition, 105, 20))
        self.FontLabel.setFont(font)
        self.FontLabel.setObjectName("FontLabel")

        self.FontComboBox = QtWidgets.QFontComboBox(self.centralwidget)
        self.FontComboBox.setGeometry(QtCore.QRect(510,  buttonPosition, 115, 20))
        self.FontComboBox.setObjectName("FontComboBox")

        #Font Size SpinBox and Font Size Label added
        self.FontSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.FontSizeLabel.setText("Font Büyüklüğü")
        self.FontSizeLabel.setGeometry(QtCore.QRect(630,  buttonPosition, 125, 20))
        self.FontSizeLabel.setFont(font)
        self.FontSizeLabel.setObjectName("FontSizeLabel")

        self.FontSizeSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.FontSizeSpinBox.setRange(10, 20)
        self.FontSizeSpinBox.setGeometry(QtCore.QRect(730,  buttonPosition, 135, 20))
        self.FontSizeSpinBox.setObjectName("FontSizeSpinBox")

        #Graphic dpi Combobox and Label added
        self.DpiLabel = QtWidgets.QLabel(self.centralwidget)
        self.DpiLabel.setText("Grafik Kalitesi(dpi)")
        self.DpiLabel.setGeometry(QtCore.QRect(870,  buttonPosition, 125, 20))
        self.DpiLabel.setFont(font)
        self.DpiLabel.setObjectName("DpiLabel")

        self.DpiComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.DpiComboBox.setGeometry(QtCore.QRect(1000,  buttonPosition, 135, 20))
        self.DpiComboBox.setObjectName("DpiComboBox")

        self.DpiComboBox.addItem("150")
        self.DpiComboBox.addItem("300")
        self.DpiComboBox.addItem("600")

        #σ(Sn) Graphic CheckBox added
        self.GraphicTypeCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.GraphicTypeCheckBox.setText("σ(Sn)")
        self.GraphicTypeCheckBox.setGeometry(QtCore.QRect(1140, buttonPosition, 85, 20))
        self.GraphicTypeCheckBox.setFont(font)
        self.GraphicTypeCheckBox.setObjectName("GraphicTypeCheckBox")

        # draw graphic button added
        self.GraphicButton = QtWidgets.QPushButton(self.centralwidget)
        self.GraphicButton.setText("Grafik Çiz")
        self.GraphicButton.setGeometry(QtCore.QRect(1210, buttonPosition, 85, 20))
        self.GraphicButton.setObjectName("GraphicButton")
        self.GraphicButton.clicked.connect(self.drawGraphic)

        # Window move to active screeen center
        fg = BigResultWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        BigResultWindow.move(fg.topLeft())

        self.retranslateUi(BigResultWindow)
        QtCore.QMetaObject.connectSlotsByName(BigResultWindow)

        if self.wasOpened == 1:
            self.FieldsLabel.setVisible(False)
            self.FieldsCombobox.setVisible(False)
            self.GraphicButton.setVisible(False)
            self.FontLabel.setVisible(False)
            self.FontComboBox.setVisible(False)
            self.FontSizeLabel.setVisible(False)
            self.FontSizeSpinBox.setVisible(False)
            self.DpiLabel.setVisible(False)
            self.DpiComboBox.setVisible(False)
            self.GraphicTypeCheckBox.setVisible(False)

        self.ResultTable.setModel(model)
        itemcount = 0
        for i in range(1, len(self.resultframe.columns.values)):
            if self.resultframe.columns.values[i].find('σ') == -1:
                self.FieldsCombobox.addItem(self.resultframe.columns.values[i][0:self.resultframe.columns.values[i].find(' ')])
                item = self.FieldsCombobox.model().item(itemcount)
                item.setCheckState(QtCore.Qt.Unchecked)
                itemcount += 1
        self.FieldsCombobox.addItem("Hepsi")
        item = self.FieldsCombobox.model().item(itemcount)
        item.setCheckState(QtCore.Qt.Unchecked)


    def retranslateUi(self, BigResultWindow):
        _translate = QtCore.QCoreApplication.translate
        BigResultWindow.setWindowTitle(_translate("BigResultWindow", "Sonuç Ekranı"))


