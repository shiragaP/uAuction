import sys
from datetime import datetime

import psycopg2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic

from chimera.Auctions import Auctions
from chimera.Users import Users


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id=0, parent=None, DEBUGMODE=False):
        super().__init__(parent) #, QtCore.Qt.FramelessWindowHint)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        form = uic.loadUi('ui\\mainwindow.ui')

        self.label_logo = form.findChild(QtWidgets.QWidget, 'label_logo')
        pixmap = QtGui.QPixmap("..\\resources\\img\\logo.png")
        self.label_logo.setPixmap(QtGui.QPixmap("..\\resources\\img\\logo.png").scaled(self.label_logo.size(), QtCore.Qt.KeepAspectRatio))

        self.pushButton_search = form.findChild(QtWidgets.QPushButton, 'pushButton_search')
        self.lineEdit_search = form.findChild(QtWidgets.QLineEdit, 'lineEdit_search')

        self.pushButton_next = form.findChild(QtWidgets.QPushButton, 'pushButton_next')
        self.pushButton_p1 = form.findChild(QtWidgets.QPushButton, 'pushButton_p1')
        self.pushButton_p2 = form.findChild(QtWidgets.QPushButton, 'pushButton_p2')
        self.pushButton_p3 = form.findChild(QtWidgets.QPushButton, 'pushButton_p3')
        self.pushButton_p4 = form.findChild(QtWidgets.QPushButton, 'pushButton_p4')
        self.pushButton_p5 = form.findChild(QtWidgets.QPushButton, 'pushButton_p5')
        self.pushButton_prev = form.findChild(QtWidgets.QPushButton, 'pushButton_prev')

        self.label_cat_1 = form.findChild(QtWidgets.QLabel, 'label_cat_1')
        self.label_cat_2 = form.findChild(QtWidgets.QLabel, 'label_cat_2')
        self.label_cat_3 = form.findChild(QtWidgets.QLabel, 'label_cat_3')
        self.label_cat_4 = form.findChild(QtWidgets.QLabel, 'label_cat_4')
        self.label_cat_5 = form.findChild(QtWidgets.QLabel, 'label_cat_5')
        self.label_cat_6 = form.findChild(QtWidgets.QLabel, 'label_cat_6')
        self.label_cat_7 = form.findChild(QtWidgets.QLabel, 'label_cat_7')
        self.label_cat_8 = form.findChild(QtWidgets.QLabel, 'label_cat_8')
        self.label_cat_9 = form.findChild(QtWidgets.QLabel, 'label_cat_9')
        self.label_cat_10 = form.findChild(QtWidgets.QLabel, 'label_cat_10')

        self.widget_login = form.findChild(QtWidgets.QWidget, 'widget_login')
        self.lineEdit_user = form.findChild(QtWidgets.QLineEdit, 'lineEdit_user')
        self.lineEdit_pass = form.findChild(QtWidgets.QLineEdit, 'lineEdit_pass')
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton_login = form.findChild(QtWidgets.QPushButton, 'pushButton_login')
        self.pushButton_login.clicked.connect(self.loginClickedActionListener)
        self.pushButton_register = form.findChild(QtWidgets.QPushButton, 'pushButton_register')

        self.widget_info = form.findChild(QtWidgets.QWidget, 'widget_info')
        self.label_name = form.findChild(QtWidgets.QLabel, 'label_name')
        self.label_user = form.findChild(QtWidgets.QLabel, 'label_user')
        self.label_userid = form.findChild(QtWidgets.QLabel, 'label_userid')

        self.pushButton_sell = form.findChild(QtWidgets.QPushButton, 'pushButton_sell')
        self.pushButton_seeprofile = form.findChild(QtWidgets.QPushButton, 'pushButton_seeprofile')
        self.pushButton_seebidhistory = form.findChild(QtWidgets.QPushButton, 'pushButton_seebidhistory')
        self.pushButton_logout = form.findChild(QtWidgets.QPushButton, 'pushButton_logout')
        self.pushButton_logout.clicked.connect(self.logoutClickedActionListener)

        self.setCentralWidget(form)

        self.setMinimumSize(form.size())
        self.setWindowIcon(QtGui.QIcon('..\\resources\\img\\icon.png'))
        self.setWindowTitle("uAuction")

        self.showGuestWidgets()
        self.loadRecentItems()

    def loadRecentItems(self):
        '''
        current_time = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
        cur = conn.cursor()
        #cur.execute("SELECT * from auctions WHERE expirytime>%s", (current_time,))
        cur.execute("SELECT * from auctions")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        self.itemCount = min(len(rows), 20)

        print(self.itemCount)
        if self.itemCount == 0:
            return

        if self.itemCount <= int((self.width() - 190) / 196):
            self.table_columnCount = self.itemCount
            self.table_rowCount = 1
        else:
            self.table_columnCount = int((self.width() - 190) / 196)
            self.table_rowCount = math.ceil(self.itemCount / self.table_columnCount)

        self.table_widget.setRowCount(self.table_rowCount)
        self.table_widget.setColumnCount(self.table_columnCount)
        for i in range(self.itemCount):
            self.table_widget.setCellWidget(int(i / self.table_columnCount), i % self.table_columnCount,
                                            ThumbnailDetailWidget(self.user_id, rows[i][0], self, DEBUGMODE=True))

        remainCellCount = (self.table_columnCount - self.itemCount % self.table_columnCount) % self.table_columnCount
        for i in range(remainCellCount):
            self.table_widget.setCellWidget(self.table_rowCount - 1, self.table_columnCount - i - 1, QtGui.QLabel())

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()'''
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)

        pass

    def loginClickedActionListener(self):
        if self.lineEdit_user.text() == "" or self.lineEdit_pass.text() =="":
            QtWidgets.QMessageBox.warning(self, "Invalid Login", "Please enter the username and the password.")
            return
        self.user_id = Users().validUser(self.lineEdit_user.text(), self.lineEdit_pass.text())
        if self.user_id > 0:
            self.login(Users().getUser(self.user_id))
        else:
            self.user_id = 0
            self.showGuestWidgets()

    def login(self, user):
        self.label_name.setText(user.firstname)
        self.label_user.setText(user.username)
        self.label_userid.setText("(" + ("%04d" % user.user_id) + ")")
        self.showUserWidgets()

    def logoutClickedActionListener(self):
        self.user_id = 0
        self.showGuestWidgets()

    def showGuestWidgets(self):
        self.lineEdit_user.setText('')
        self.lineEdit_pass.setText('')

        self.widget_info.hide()
        self.pushButton_sell.hide()
        self.pushButton_seeprofile.hide()
        self.pushButton_seebidhistory.hide()
        self.pushButton_logout.hide()

        self.widget_login.show()
        self.pushButton_login.show()
        self.pushButton_register.show()

    def showUserWidgets(self):
        self.widget_login.hide()
        self.pushButton_login.hide()
        self.pushButton_register.hide()

        self.widget_info.show()
        self.pushButton_sell.show()
        self.pushButton_seeprofile.show()
        self.pushButton_seebidhistory.show()
        self.pushButton_logout.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(DEBUGMODE=True)
    window.show()
    app.exec_()
