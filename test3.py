import signal
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class EventFilter(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eventFilter(self, obj, event):
        # if isinstance(event, QtCore.QTimerEvent):
        #     return True
        # elif isinstance(event, QtCore.QChildEvent):
        #     print("Event:", obj, event.child())
        #     if isinstance(event.child(), QtCore.QObject):
        #         print(event.child().objectName())
        #     return True
        # else:
        print("eventFilter", obj, event)
        return super().eventFilter(obj, event)
    
class TestItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TestModel(QtGui.QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
        self.event_filter = EventFilter(self)
        self.installEventFilter(self.event_filter) #keyboard control

class MainWindow(QtWidgets.QMainWindow):
    def changed(self, *args):
        print("changed", args)
    def inserted(self, *args):
        print("inserted", args)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

        
        self.list_view = QtWidgets.QListView()
        
        
        self.setCentralWidget(self.list_view)
        self.list_view.show()

        self.model = TestModel()
        self.model.itemChanged.connect(self.changed)
        self.model.rowsInserted.connect(self.inserted)
        self.list_view.setModel(self.model)
        
        item = TestItem("1")
        self.model.appendRow(item)
        item = TestItem("2")
        self.model.appendRow(item)

class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)

        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)    
    sys.exit(app.exec_())


