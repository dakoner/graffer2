# -*- coding: utf-8 -*-

# from PySide2 import QtCore  # type: ignore
# from PySide2 import QtGui  # type: ignore
# from PySide2 import QtWidgets  # type: ignore
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.uic import loadUi
import signal
import sys


class Edge(QtWidgets.QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 10))
        
class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)
        self.setPen(QtGui.QPen(QtCore.Qt.red, 1))
        self.setBrush(QtCore.Qt.blue)
        self.setFlags(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges | QtWidgets.QGraphicsItem.ItemIsMovable)

    def __str__(self):
        return self.name
    
class GraphNodeListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            t = self.nodes[index.row()]
            return str(t)
        
    def add_node(self, node):
        self.nodes.append(node)

    def __len__(self):
        return len(self.nodes)
    
    def rowCount(self, index):
        return len(self)
    
class GraphScene(QtWidgets.QGraphicsScene):
    def __init__(self, graphicsView, listView, *args, **kwargs):
        self.graphicsView = graphicsView
        self.listView = listView
        self.model = GraphNodeListModel()
        self.listView.setModel(self.model)

        super().__init__(*args, **kwargs)



    # def mouseMoveEvent(self, event):
    #     print("scene mouse move event", event.scenePos())
    #     return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        print("scene mouse press event", event)
        item = self.itemAt(event.scenePos(), QtGui.QTransform())
        print(item)
        if item is None:
            l = len(self.model)
            name = f"Node"
            print("Add new", name)
            item = Node(name, 0, 0, 10, 10)
            print(event.scenePos())
            item.setPos(event.scenePos())
            self.addItem(item)
            self.model.add_node(item)
            self.model.rowsInserted.emit(QtCore.QModelIndex(), l, l)
            print([item.pos() for item in self.items()])
            self.graphicsView.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
        return super().mousePressEvent(event)
        
        
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("graffer2.ui", self)

        self.listView = self.findChild(QtWidgets.QListView, "listView")
        self.graphicsView = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        self.scene = GraphScene(self.graphicsView, self.listView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(0, 0, 100, 100)
        self.graphicsView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        #self.graphicsView.setMouseTracking(True)

    def resizeEvent(self, *args):
        self.graphicsView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        return super().resizeEvent(*args)


class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)

        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)    
    app.exec_()
