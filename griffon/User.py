__author__ = 'Fujiwara'

import sys

import psycopg2
from PySide import QtGui
from PySide import QtUiTools

import DatabaseInfo
from griffon.AddAuction import AddAuctionDialog


class User():
    def __init__(self, user_id):
        self.user_id = user_id

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        cur.execute("SELECT * from users WHERE users.id=%s", (self.user_id,))

        row = cur.fetchall()[0]
        self.username = row[1]
        self.password = row[2]
        self.email = row[3]
        self.firstname = row[4]
        self.lastname = row[5]
        self.address1 = row[6]
        self.address2 = row[7]
        self.province = row[8]
        self.country = row[9]
        self.zipcode = row[10]
        self.phone = row[11]
        conn.commit()

        cur.close()
        conn.close()


class UserWidget(QtGui.QWidget):
    def __init__(self, user_id=1, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.user = User(self.user_id)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\user.ui')

        self.label_username = form.findChild(QtGui.QLabel, 'label_01_username')
        self.label_email = form.findChild(QtGui.QLabel, 'label_04_email')
        self.label_firstname = form.findChild(QtGui.QLabel, 'label_05_firstname')
        self.label_lastname = form.findChild(QtGui.QLabel, 'label_06_lastname')
        self.label_address1 = form.findChild(QtGui.QLabel, 'label_07_address1')
        self.label_address2 = form.findChild(QtGui.QLabel, 'label_08_address2')
        self.label_province = form.findChild(QtGui.QLabel, 'label_09_province')
        self.label_country = form.findChild(QtGui.QLabel, 'label_10_country')
        self.label_zipcode = form.findChild(QtGui.QLabel, 'label_11_zipcode')
        self.label_phonenumber = form.findChild(QtGui.QLabel, 'label_12_phonenumber')

        self.pushButton_sellitem = form.findChild(QtGui.QPushButton, 'pushButton_01_sellitem')
        self.pushButton_seebidhistory = form.findChild(QtGui.QPushButton, 'pushButton_02_seebidhistory')
        self.pushButton_logout = form.findChild(QtGui.QPushButton, 'pushButton_03_logout')

        self.label_username.setText(self.user.username)
        self.label_email.setText(self.user.email)
        self.label_firstname.setText(self.user.firstname)
        self.label_lastname.setText(self.user.lastname)
        self.label_address1.setText(self.user.address1)
        self.label_address2.setText(self.user.address2)
        self.label_province.setText(self.user.province)
        self.label_country.setText(self.user.country)
        self.label_zipcode.setText(self.user.zipcode)
        self.label_phonenumber.setText(self.user.phone)

        self.label_address1.setText('<p style=\"line-height:125\">' + self.label_address1.text() + '<p>')
        self.label_address1.setWordWrap(True)
        self.label_address2.setText('<p style=\"line-height:125\">' + self.label_address2.text() + '<p>')
        self.label_address2.setWordWrap(True)

        self.pushButton_sellitem.clicked.connect(self.sellActionListener)
        self.pushButton_seebidhistory.clicked.connect(self.seeBidHistoryActionListener)
        self.pushButton_logout.clicked.connect(self.logoutActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('User ' + str(self.user_id))

    def sellActionListener(self):
        addAuctioDialog = AddAuctionDialog(user_id=self.user_id, DEBUGMODE=True)
        addAuctioDialog.exec_()

    def seeBidHistoryActionListener(self):
        # todo
        #bidHistoryDialog = BidHistoryDialog(user_id=self.user_id, DEBUGMODE=True)
        #bidHistoryDialog.exec_()
        pass

    def logoutActionListener(self):
        if self.parent is not None:
            self.parent.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    userWidget = UserWidget(DEBUGMODE=True)
    userWidget.show()
    sys.exit(app.exec_())