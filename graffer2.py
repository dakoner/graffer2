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

    def mousePressEvent(self, event):
        print("mouse press event", self, event)
        return super().mousePressEvent(event)
        
    # def mouseReleaseEvent(self, event):
    #     print("mouse relase event", event)
    #     return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        print("mouse move event", self, event)
        return super().mouseMoveEvent(event)

    # def itemChange(self, *args, **kwargs):
    #     print("itemChange", args, kwargs)
    #     # if args[0] == QtWidgets.QGraphicsItem.ItemSceneChange:
    #     #     print("Item changed", args, kwargs)
    #     # if args[0] == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
    #     #     print(f"Item {self.node} changed: {args[1]}")
    #     return super().itemChange(*args, **kwargs)


class GraphScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.G = nx.balanced_tree(2, 3)   
        pos = nx.spring_layout(self.G)


        for node in self.G.nodes():
            item = Node(0, 0, .01, .01)
            self.addItem(item)
            item.node = node
            item.setPos(*pos[node])


        for edge in self.G.edges():
            p0 = pos[edge[0]]
            p1 = pos[edge[1]]
            item = Edge(p0[0]+.025, p0[1]+.025, p1[0]+.025, p1[1]+.025)
            self.addItem(item)


    def mousePressEvent(self, event):
        print("scene mouse press event", event)
        item = self.itemAt(event.scenePos(), QtGui.QTransform())
        if item is None:
            item = Node(0, 0, .01, .01)
            self.addItem(item)
            i = max(self.G.nodes)
            self.G.add_node(i)
            item.node = i
            item.setPos(event.scenePos())
            event.accept()
        else:
            event.ignore()
        return super().mousePressEvent(event)
        
    # def mouseReleaseEvent(self, event):
    #     print("scene mouse relase event", event)
        
    #     return super().mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event):
    #     print("scene mouse move event", event)
        
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("graffer2.ui", self)

        self.scene = GraphScene()
        self.graphicsView = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        self.graphicsView.setScene(self.scene)
        
        # self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        # self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

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


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)    
    app.exec_()
