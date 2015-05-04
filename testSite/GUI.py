import sys
from Linksys import *
from Restaurant import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *


class MainWindow(QQuickView):
    def __init__(self):
        super(MainWindow, self).__init__(None)

        data = [Restaurant(self, "Uncle Steak", "", "images/14.jpg"),
                Restaurant(self, "Starbucks", "", "images/15.jpg"),
                Restaurant(self, "Pancake Cafe", "", "images/16.jpg"),
                Restaurant(self, "Yoshi", "", "images/17.jpg")]

        self.wrapper = MainWrapper(self, data)
        self.linksys = Linksys()
        self.context = self.rootContext()
        self.context.setContextProperty("linksys", self.linksys)
        self.context.setContextProperty("wrapper", self.wrapper)

        self.setTitle("Main Window")
        self.setSource(QUrl.fromLocalFile('home.qml'))
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())