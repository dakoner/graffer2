import signal
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


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

    # def mousePressEvent(self, event):
    #     print("mouse press event", event)
    #     return super().mousePressEvent(event)
        
    # def mouseReleaseEvent(self, event):
    #     print("mouse relase event", event)
    #     return super().mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event):
    #     print("mouse move event", event)
    #     return super().mouseMoveEvent(event)

    # def itemChange(self, *args, **kwargs):
    #     print("itemChange", args, kwargs)
    #     if args[0] == QtWidgets.QGraphicsItem.ItemSceneChange:
    #         print("Item changed", args, kwargs)
    #     if args[0] == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
    #         print(f"Item {self.node} changed: {args[1]}")
    #     return super().itemChange(*args, **kwargs)


class EventFilter(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eventFilter(self, obj, event):
        print("eventFilter", obj, event)
        if type(event) == QtCore.QDynamicPropertyChangeEvent:
            print("Event:", dir(event))
            print(event.propertyName())
        return True

class TestObject(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.event_filter = EventFilter(self)
        self.installEventFilter(self.event_filter) #keyboard control


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtCore.QCoreApplication(sys.argv)
    to = TestObject(app)
    to.setProperty("foo", "bar")
    print(dir(to))
    sys.exit(app.exec_())
