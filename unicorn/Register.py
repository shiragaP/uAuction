__author__ = 'Shiraga-P'

import sys

import psycopg2
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

import DatabaseInfo


class RegisterWidget(QtGui.QWidget):
    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\register.ui')

        self.lineEdit_username = form.findChild(QtGui.QLineEdit, 'lineEdit_01_username')
        self.lineEdit_username.setMaxLength(12)
        self.lineEdit_password = form.findChild(QtGui.QLineEdit, 'lineEdit_02_password')
        self.lineEdit_password.setMaxLength(12)
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_repassword = form.findChild(QtGui.QLineEdit, 'lineEdit_03_repassword')
        self.lineEdit_repassword.setMaxLength(12)
        self.lineEdit_repassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_email = form.findChild(QtGui.QLineEdit, 'lineEdit_04_email')
        self.lineEdit_email.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_firstname = form.findChild(QtGui.QLineEdit, 'lineEdit_05_firstname')
        self.lineEdit_firstname.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_lastname = form.findChild(QtGui.QLineEdit, 'lineEdit_06_lastname')
        self.lineEdit_lastname.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_address1 = form.findChild(QtGui.QLineEdit, 'lineEdit_07_address1')
        self.lineEdit_address1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_address2 = form.findChild(QtGui.QLineEdit, 'lineEdit_08_address2')
        self.lineEdit_address2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_province = form.findChild(QtGui.QLineEdit, 'lineEdit_09_province')
        self.lineEdit_province.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_country = form.findChild(QtGui.QLineEdit, 'lineEdit_10_country')
        self.lineEdit_country.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_zipcode = form.findChild(QtGui.QLineEdit, 'lineEdit_11_zipcode')
        self.lineEdit_zipcode.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{0,28}"), self))

        self.pushButton_register = form.findChild(QtGui.QPushButton, 'pushButton_register')
        self.pushButton_register.clicked.connect(self.registerActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)

    def registerActionListener(self):
        # TODO: validation
        invalidFlags = list()

        username = self.lineEdit_username.text()
        if 4 > len(username):
            invalidFlags.append('username')

        password = self.lineEdit_password.text()
        if 4 > len(password):
            invalidFlags.append('password')
        if 'password' not in invalidFlags and password != self.lineEdit_repassword.text():
            invalidFlags.append('repassword')

        firstname = self.lineEdit_firstname.text()
        if not firstname:
            invalidFlags.append('firstname')

        lastname = self.lineEdit_lastname.text()
        if not lastname:
            invalidFlags.append('lastname')

        address1 = self.lineEdit_address1.text()
        if not address1:
            invalidFlags.append('address1')
        address2 = self.lineEdit_address2.text()

        province = self.lineEdit_province.text()
        if not province:
            invalidFlags.append('province')

        country = self.lineEdit_country.text()
        if not country:
            invalidFlags.append('country')

        zipcode = self.lineEdit_zipcode.text()
        if not zipcode:
            invalidFlags.append('zipcode')

        self.register(username, password, firstname, lastname, address1, address2, province, country, zipcode)

    def register(self, username, password, firstname, lastname, address1, address2, province, country, zipcode):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
                                % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        statement = ""
        statement += """INSERT INTO users (username, password, firstname, lastname, address1, address2, province, country, zipcode)
                        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                        """ % (username, password, firstname, lastname, address1, address2, province, country, zipcode)

        if (self.DEBUGMODE):
            print("Sql Statement")
            print(statement)

        cur.execute(statement)
        conn.commit()
        cur.close()
        conn.close()
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    registerWidget = RegisterWidget(DEBUGMODE=True)
    registerWidget.show()
    sys.exit(app.exec_())