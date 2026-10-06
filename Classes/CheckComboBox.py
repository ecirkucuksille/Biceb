from PyQt5.QtWidgets import QComboBox, QListView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

class QCheckComboBox(QComboBox):
    def __init__(self, parent = None):
        super(QCheckComboBox, self).__init__(parent)
        self.setView(QListView(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def checkedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == Qt.Checked:
                checkedItems.append(item)
        return checkedItems

    def checkedIndex(self):
        checkedIndex = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == Qt.Checked:
                checkedIndex.append(index)
        return checkedIndex

    def getValueFromIndex(self, index):
        item = self.model().item(index)
        return item.text()

    def getAllIndices(self):
        allIndices = []
        for index in range(self.count() - 1):
            allIndices.append(index)
        return allIndices