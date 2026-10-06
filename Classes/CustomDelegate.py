from PyQt5 import QtCore,QtWidgets, QtGui

class QCustomDelegate (QtWidgets.QItemDelegate):
    controlcolumn = -1
    def paint (self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex):
        row = indexQModelIndex.row()
        col =  indexQModelIndex.column()
        if row == self.controlcolumn:
            textQString = indexQModelIndex.model().data(indexQModelIndex).value()
            newfont = QtGui.QFont("Tahoma", 10,QtGui.QFont.Bold)
            painterQPainter.setFont(newfont)
            painterQPainter.fillRect(optionQStyleOptionViewItem.rect, QtGui.QColor('#F0EEEB'))
            painterQPainter.drawText(optionQStyleOptionViewItem.rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, textQString)
        elif col == 0:
            textQString = indexQModelIndex.model().data(indexQModelIndex).value()
            newfont = QtGui.QFont("Tahoma", 10,QtGui.QFont.Bold)
            newfont.setItalic(True)
            painterQPainter.setFont(newfont)
            painterQPainter.fillRect(optionQStyleOptionViewItem.rect, QtGui.QColor('#F0EEEB'))
            painterQPainter.drawText(optionQStyleOptionViewItem.rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, textQString)
        else:
            QtWidgets.QItemDelegate.paint(self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex)
