__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from unicorn import Login, Account

from PySide import QtGui
from PySide import QtUiTools


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE
        self.label = QtGui.QLabel("This is MainWindow ;)\nComing Soon!!!")
        self.setCentralWidget(self.label)

    def run(self, username):
        self.username = username
        self.account = Account.User(username)
        self.show()

    def login(self):
        loginWidget = Login.LoginWidget(self)
        loginWidget.exec_()





if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(DEBUGMODE=True)
    mainWindow.login()
    sys.exit(app.exec_())