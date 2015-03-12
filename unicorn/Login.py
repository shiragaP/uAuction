__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from PySide import QtGui
from PySide import QtUiTools


class LoginWidget(QtGui.QDialog):
    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
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

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        rows = cur.fetchall()

        if (self.DEBUGMODE):
            print('Show me the databases:')
            for row in rows:
                print(row)

        loginValid = False
        for row in rows:
            print("Comparing username:", row[1], username, str(row[1]) == username)
            print("Comparing password:", row[2], password, str(row[2]) == password)
            if str(row[1]) == username and str(row[2]) == password:
                loginValid = True
                break

        if loginValid:
            if __name__ != '__main__':
                self.parent.run(username)
            self.close()
        else:
            QtGui.QMessageBox.warning(self, "Notification", "Invalid username and/or password")



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = LoginWidget(DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())