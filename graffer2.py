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
import networkx as nx

import preditor

class Edge(QtWidgets.QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0.001))
        
class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(QtGui.QPen(QtCore.Qt.darkMagenta, 0.01))
        #self.setBrush(QtGui.QGradient(QtGui.QGradient.SaintPetersburg))
        self.setFlags(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges | QtWidgets.QGraphicsItem.ItemIsMovable)

class GraphNodeListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.G = nx.Graph()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            t = list(self.G.nodes())[index.row()]
            return t.name
        
    def rowCount(self, index):
        return len(self.G.nodes)
    
class GraphScene(QtWidgets.QGraphicsScene):
    def __init__(self, listView, *args, **kwargs):
        self.listView = listView
        self.model = GraphNodeListModel()
        self.listView.setModel(self.model)

        super().__init__(*args, **kwargs)


    def addGraph(self, g, pos):

        nodemap = {}
        for node in g.nodes():
            item = Node(0, 0, .01, .01)
            item.name = f"Node {node}"
            item.setPos(*pos[node])
            self.addItem(item)
            nodemap[node] = item            
            self.model.G.add_node(item)

        for edge in g.edges():
            p0 = pos[edge[0]]
            p1 = pos[edge[1]]
            item = Edge(p0[0]+.025, p0[1]+.025, p1[0]+.025, p1[1]+.025)
            self.addItem(item)

            self.model.G.add_edge(nodemap[edge[0]], nodemap[edge[1]])

        self.model.rowsInserted.emit(QtCore.QModelIndex(), 0, len(g.nodes()))

    def mousePressEvent(self, event):
        print("scene mouse press event", event)
        item = self.itemAt(event.scenePos(), QtGui.QTransform())
        if item is None:
            item = Node(0, 0, .01, .01)
            item.setPos(event.scenePos())
            self.addItem(item)

            self.model.G.add_node(item)
            l = len(self.model.G.nodes())-1
            item.name = f"Node {l}"
            self.model.rowsInserted.emit(QtCore.QModelIndex(), l, l)
           
        return super().mousePressEvent(event)
        
        
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("graffer2.ui", self)

        self.listView = self.findChild(QtWidgets.QListView, "listView")
        self.scene = GraphScene(self.listView)
        self.graphicsView = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        self.graphicsView.setScene(self.scene)
        self.loggerDockWidget = self.findChild(QtWidgets.QDockWidget, "dockWidget_3")
        preditor.configure("editor")
        self.preditor = preditor.launch()
        self.loggerDockWidget.setWidget(self.preditor)

        self.graphicsView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, *args):
        self.graphicsView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        return super().resizeEvent(*args)


class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)

        self.main_window = MainWindow()
        self.main_window.show()

        G = nx.balanced_tree(2, 3)
        #G = nx.Graph()
        #G.add_node(1)   
        pos = nx.spring_layout(G)
        self.main_window.graphicsView.scene().addGraph(G, pos)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)    
    app.exec_()
