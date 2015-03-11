__author__ = 'Shiraga-P'

import sys

from PySide import QtGui
from PySide import QtUiTools

class LoginWidget(QtGui.QWidget):

    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\login.ui')

        self.label_logo = form.findChild(QtGui.QLabel, 'label_00_logo')
        self.label_logo.setPixmap(QtGui.QPixmap('..\\resources\\img\\logo.png'))

        self.lineEdit_username = form.findChild(QtGui.QLineEdit, 'lineEdit_01_username')
        self.lineEdit_password = form.findChild(QtGui.QLineEdit, 'lineEdit_02_password')
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)

        self.pushButton_login = form.findChild(QtGui.QPushButton, 'pushButton_login')
        self.pushButton_login.clicked.connect(self.loginActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Login')

    def loginActionListener(self):
        if(self.DEBUGMODE):
            print("Login")
            print("\tUsername: " + self.lineEdit_username.text())
            print("\tPassword: " + self.lineEdit_password.text())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = LoginWidget(DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())