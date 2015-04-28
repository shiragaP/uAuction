__author__ = 'Waterstrider'
import sys

from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView


# Main Function
if __name__ == '__main__':
    # Create main app
    myApp = QApplication(sys.argv)
    # Create a label and set its properties
    appLabel = QQuickView()
    appLabel.setSource(QUrl('Mainwindow.qml'))
    rc = appLabel.rootContext()

    class Link(QObject):
        def __init__(self):
            super().__init__()

        # @QtCore.pyqtSlot(int)
        @pyqtSlot('QString')
        def debug(self, s):
            print(s)

    link = Link()
    rc.setContextProperty('link', link)
    # Show the Label
    appLabel.show()

    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()