

## To waterslider

# create widget ui from ui/register.ui
# link every lineEdit to string
# when button pressed validate for each string according to example and explaination
# have bool to store for validation

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
        self.lineEdit_repassword = form.findChild(QtGui.QLineEdit, 'lineEdit_03_repassword')
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
        pass

    def register(self, username, password, firstname, lastname, address1, address2, province, country, zipcode):
        con = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
                               % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = con.cursor()

        statement = ""
        statement += """INSERT INTO users (username, password, firstname, lastname, address1, address2, province, country, zipcode)
                        VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                     % (username, password, firstname, lastname, address1, address2, province, country, zipcode)

        cur.execute(statement)
        cur.close()
        con.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    registerWidget = RegisterWidget(DEBUGMODE=True)
    registerWidget.show()
    sys.exit(app.exec_())