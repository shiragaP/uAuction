import sys, math
from datetime import datetime, timedelta

import psycopg2
from PySide import QtCore
from PySide import QtGui

from unicorn.ThumbnailDetail import ThumbnailDetailWidget
from unicorn.User import UserWidget
import DatabaseInfo


class MainWindow(QtGui.QMainWindow):

    def __init__(self, user_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.centralwidget = QtGui.QWidget(parent)
        self.centralwidget.setObjectName("centralwidget")

        #======================== Menu Bar ========================
        self.menu_bar = QtGui.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 780, 20))

        self.menu_file = QtGui.QMenu("File", self.menu_bar)
        self.menu_help = QtGui.QMenu("Help", self.menu_bar)
        self.setMenuBar(self.menu_bar)

        self.action_exit = QtGui.QAction("Exit", self)
        self.action_about = QtGui.QAction("About", self)

        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        #======================== Menu Bar Connection ========================
        self.action_exit.triggered.connect(self.close)

        #======================== Statue Bar ========================
        self.status_bar = QtGui.QStatusBar(parent)
        self.setStatusBar(self.status_bar)


        self.banner = QtGui.QLabel(self)
        self.banner.setGeometry(QtCore.QRect(170 + 2, 15 + 12, 600, 140))
        self.banner.setPixmap(QtGui.QPixmap('..\\resources\\img\\nobanner.png'))

        self.banner.setAlignment(QtCore.Qt.AlignCenter)

        self.table_widget = QtGui.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(170, 175, 590 + 17, 395))
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        self.user_widget = UserWidget(self.user_id, self)
        self.user_widget.setGeometry(QtCore.QRect(5, 15, 160, 555))

        self.loadRecentItems()

        self.resize(790, 580)
        self.setMinimumSize(790, 580)
        self.setWindowTitle("uAuction")

    def loadRecentItems(self):
        current_time = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from items WHERE expirytime>%s", (current_time,))
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        self.table_widget.clear()
        self.itemCount = min(len(rows), 20)
        if self.itemCount <= int((self.width() - 190)/196):
            self.table_columnCount = self.itemCount
            self.table_rowCount = 1
        else:
            self.table_columnCount = int((self.width() - 190)/196)
            self.table_rowCount = math.ceil(self.itemCount/self.table_columnCount)

        self.table_widget.setRowCount(self.table_rowCount)
        self.table_widget.setColumnCount(self.table_columnCount)
        for i in range(self.itemCount):
            self.table_widget.setCellWidget(int(i/self.table_columnCount), i % self.table_columnCount, ThumbnailDetailWidget(self.user_id, i + 1, self, DEBUGMODE=True))

        remainCellCount = (self.table_columnCount - self.itemCount%self.table_columnCount) % self.table_columnCount
        for i in range(remainCellCount):
            self.table_widget.setCellWidget(self.table_rowCount - 1, self.table_columnCount - i - 1, QtGui.QLabel())

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.banner.setGeometry(QtCore.QRect(165 + 2, 15 + 12, self.width() - 195 + 17 + 10, 140))
        self.table_widget.setGeometry(QtCore.QRect(170, 175, self.width() - 195 + 17, self.height() - 185))

        self.loadRecentItems()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(1, DEBUGMODE=True)
    window.show()
    app.exec_()
