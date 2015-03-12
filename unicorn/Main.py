__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from unicorn import Login

from PySide import QtGui
from PySide import QtUiTools


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE

        self.label = QtGui.QLabel("Test")
        self.setCentralWidget(self.label)

    def login(self):
        loginWidget = Login.LoginWidget(self)
        loginWidget.exec_()





if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(DEBUGMODE=True)
    mainWindow.login()
    sys.exit(app.exec_())