__author__ = 'Shiraga-P'

import sys

from PySide import QtGui

from unicorn.Login import LoginDialog
from unicorn.MainWindow import MainWindow


class Main():
    def __init__(self, parent=None, DEBUGMODE=False):
        self.DEBUGMODE = DEBUGMODE

    def run(self, user_id):
        self.mainWindow = MainWindow(user_id)
        self.mainWindow.show()

    def login(self):
        loginDialog = LoginDialog(self)
        loginDialog.exec_()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = Main(DEBUGMODE=True)
    mainWindow.login()
    sys.exit(app.exec_())