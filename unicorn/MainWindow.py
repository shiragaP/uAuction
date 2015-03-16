import sys

from PySide import QtCore
from PySide import QtGui

from unicorn.User import UserWidget


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
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 650, 20))

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

        #QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL("triggered()"), super().close)
        #QtCore.QObject.connect(self.action_about, QtCore.SIGNAL("triggered()"), self.about)

        #======================== Statue Bar ========================
        self.status_bar = QtGui.QStatusBar(parent)
        self.setStatusBar(self.status_bar)


        self.banner = QtGui.QLabel(self.centralwidget)
        self.banner.setGeometry(QtCore.QRect(10, 15, 590, 140))
        self.banner.setAlignment(QtCore.Qt.AlignCenter)

        self.table_widget = QtGui.QLabel(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(10, 175, 590, 395))

        self.user_widget = UserWidget(self.user_id, self)
        self.user_widget.setGeometry(QtCore.QRect(610, 15, 160, 555))

        self.resize(780, 580)
        self.setWindowTitle("uAuction")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(1, DEBUGMODE=True)
    window.show()
    app.exec_()
