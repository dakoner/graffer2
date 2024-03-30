# -*- coding: utf-8 -*-

# from PySide2 import QtCore  # type: ignore
# from PySide2 import QtGui  # type: ignore
# from PySide2 import QtWidgets  # type: ignore
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.uic import loadUi
import networkx as nx
import signal
import sys


        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("test_ui_model.ui", self)


        self.model = QtGui.QStandardItemModel (4, 4)
        for row in range(4):
            for column in range(4):
                item = QtGui.QStandardItem("row %d, column %d" % (row, column))
                self.model.setItem(row, column, item)

        self.listView = self.findChild(QtWidgets.QListView, "listView")
        self.listView.setModel(self.model)
        self.listView.setAcceptDrops(True)
        self.listView.setDragEnabled(True)
        self.listView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        self.tableView = self.findChild(QtWidgets.QTableView, "tableView")
        self.tableView.setModel(self.model)
        self.tableView.setAcceptDrops(True)
        self.tableView.setDragEnabled(True)
        self.tableView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)

        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)    
    app.exec_()
