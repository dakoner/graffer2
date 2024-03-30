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
        self.graph = nx.Graph()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            t = list(self.graph.nodes())[index.row()]
            return str(t)
        
    def add_node(self, node):
        self.graph.add_node(node)

    def __len__(self):
        return len(self.graph.nodes())
    
    def rowCount(self, index):
        return len(self)
    
class GraphScene(QtWidgets.QGraphicsScene):
    def __init__(self, graphicsView, listView, *args, **kwargs):
        self.graphicsView = graphicsView
        self.listView = listView
        self.model = GraphNodeListModel()
        self.listView.setModel(self.model)

        super().__init__(*args, **kwargs)

        item = Node("foo", 0, 0, 10, 10)
        item.setPos(50, 50)
        self.addItem(item)
        self.model.add_node(item)
        self.model.rowsInserted.emit(QtCore.QModelIndex(), 0, 0)
        self.graphicsView.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def mouseMoveEvent(self, event):
        print("scene mouse move event", event.scenePos())
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), QtGui.QTransform())
        # if there's no node at this point, and we're pressing control, add a new node
        if item is None and event.modifiers() & QtCore.Qt.ControlModifier:
            l = len(self.model)
            name = f"Node {l}"
            print("Add new", name)
            item = Node(name, 0, 0, 10, 10)
            item.setPos(event.scenePos())
            self.addItem(item)
            self.model.add_node(item)
            self.model.rowsInserted.emit(QtCore.QModelIndex(), l, l)
            # suppress drag of graphicsview when adding new node
            event.accept()
            return None
        return super().mousePressEvent(event)
        
        
class GrafferGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def mouseMoveEvent(self, event):
    #     print("qgraphicsview mouse move event", event)
    #     super().mouseMoveEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("graffer2.ui", self)

        self.listView = self.findChild(QtWidgets.QListView, "listView")
        self.graphicsView = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        self.scene = GraphScene(self.graphicsView, self.listView)
        self.graphicsView.setScene(self.scene)
        # Make scene rectangle much larger, so drag outside of on-screen view works
        self.graphicsView.setSceneRect(-1000, -1000, 2000, 2000)
        # show a region smaller than the full scene rectangle
        self.graphicsView.fitInView(-100, -100, 200, 200, QtCore.Qt.KeepAspectRatio)
        # allow dragging of the on-screen view
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

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
