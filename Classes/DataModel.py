from PyQt5 import QtCore
from PyQt5 import QtGui
import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                listvalue = self._df.columns.tolist()[section]
                if listvalue == 'Unnamed: 0':
                    return ''
                else:
                    return listvalue
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.BackgroundColorRole:
            if index.column() == 0:
                return QtCore.QVariant(QtGui.QColor('#F0EEEB'))

        if role == QtCore.Qt.FontRole:
            if index.column() == 0:
                return QtCore.QVariant(QtGui.QFont("Tahoma", 10,QtGui.QFont.Bold))

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))


    def setData(self, index, value, role):
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            pass
        if value != '':
            self._df.iat[row, col] = value
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def flags(self, index):
        if index.column() != 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
             return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable