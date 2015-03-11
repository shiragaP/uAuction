

__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from PySide import QtGui
from PySide import QtUiTools

class RegisterWidget(QtGui.QWidget):

    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\register.ui')

        self.lineEdit_username = form.findChild(QtGui.QLineEdit, 'lineEdit_01_username')
        self.lineEdit_password = form.findChild(QtGui.QLineEdit, 'lineEdit_02_password')
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_repassword = form.findChild(QtGui.QLineEdit, 'lineEdit_03_repassword')
        self.lineEdit_repassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_firstname = form.findChild(QtGui.QLineEdit, 'lineEdit_04_firstname')
        self.lineEdit_lastname = form.findChild(QtGui.QLineEdit, 'lineEdit_05_lastname')
        self.lineEdit_address1 = form.findChild(QtGui.QLineEdit, 'lineEdit_06_address1')
        self.lineEdit_address2 = form.findChild(QtGui.QLineEdit, 'lineEdit_07_address2')
        self.lineEdit_province = form.findChild(QtGui.QLineEdit, 'lineEdit_08_province')
        self.lineEdit_country = form.findChild(QtGui.QLineEdit, 'lineEdit_09_country')
        self.lineEdit_zipcode = form.findChild(QtGui.QLineEdit, 'lineEdit_10_zipcode')

        self.pushButton_register = form.findChild(QtGui.QPushButton, 'pushButton_register')
        self.pushButton_register.clicked.connect(self.registerActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)

    def registerActionListener(self):
        #TODO: validation
        self.register(self.lineEdit_username.text(),
                 self.lineEdit_password.text(),
                 self.lineEdit_firstname.text(),
                 self.lineEdit_lastname.text(),
                 self.lineEdit_address1.text(),
                 self.lineEdit_address2.text(),
                 self.lineEdit_province.text(),
                 self.lineEdit_country.text(),
                 self.lineEdit_zipcode.text())

    def register(self, username, password, firstname, lastname, address1, address2, province, country, zipcode):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
                               % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        statement = ""
        statement += """INSERT INTO users (username, password, firstname, lastname, address1, address2, province, country, zipcode)
                        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                        """ % (username, password, firstname, lastname, address1, address2, province, country, zipcode)

        if(self.DEBUGMODE):
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