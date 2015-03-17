import sys

import psycopg2
from PySide import QtCore
from PySide import QtGui

from unicorn.User import UserWidget
from unicorn.ThumbnailDetail import ThumbnailDetailWidget
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
        self.banner.setGeometry(QtCore.QRect(10 + 2, 15 + 12, 600, 140))
        self.banner.setPixmap(QtGui.QPixmap('..\\resources\\img\\nobanner.png'))
        self.banner.setAlignment(QtCore.Qt.AlignCenter)

        self.table_widget = QtGui.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(10, 175, 590 + 17, 395))
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        self.user_widget = UserWidget(self.user_id, self)
        self.user_widget.setGeometry(QtCore.QRect(615, 15, 160, 555))

        self.loadRecentItems()

        self.resize(780, 580)
        self.setMinimumSize(780, 580)
        self.setWindowTitle("uAuction")

    def loadRecentItems(self):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from items ORDER BY id DESC")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        self.table_columnCount = int(590/196)
        self.table_widget.setRowCount(int(20/self.table_columnCount) + 1)
        self.table_widget.setColumnCount(self.table_columnCount)
        for i in range(min(len(rows), 20)):
            self.table_widget.setCellWidget(int(i/self.table_columnCount), i%self.table_columnCount, ThumbnailDetailWidget(i + 1, DEBUGMODE=True))
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(1, DEBUGMODE=True)
    window.show()
    app.exec_()
