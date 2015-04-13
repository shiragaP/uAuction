__author__ = 'Shiraga-P'

import sys
import pickle
import http.client
import urllib

from PySide import QtGui
from PySide import QtUiTools


class LoginDialog(QtGui.QDialog):
    def __init__(self, main=None, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.main = main
        self.parent = parent
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
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if (self.DEBUGMODE):
            print("Login")
            print("\tUsername: " + username)
            print("\tPassword: " + password)

        conn = http.client.HTTPConnection("localhost", 8080)
        params = urllib.parse.urlencode({'statement': "SELECT * from users WHERE users.username='%s'" % (username,)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        if (self.DEBUGMODE):
            print('Show me the databases:')
            for row in rows:
                print(row)

        loginValid = False
        if rows:
            print("Comparing username:", row[1], username, str(row[1]) == username)
            print("Comparing password:", row[2], password, str(row[2]) == password)
            if str(row[1]) == username and str(row[2]) == password:
                loginValid = True
                self.user_id = row[0]
        # for row in rows:
        # print("Comparing username:", row[1], username, str(row[1]) == username)
        # print("Comparing password:", row[2], password, str(row[2]) == password)
        #     if str(row[1]) == username and str(row[2]) == password:
        #         loginValid = True
        #         self.user_id = row[0]
        #         break

        if loginValid:
            if __name__ != '__main__':
                self.main.run(self.user_id)
            self.close()
        else:
            QtGui.QMessageBox.warning(self, "Notification", "Invalid username and/or password")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = LoginDialog(DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())