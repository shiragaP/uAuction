import sys

from PySide import QtCore
from PySide import QtGui

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
        self.menu_bar.setObjectName("menu_bar")

        self.menu_file = QtGui.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtGui.QMenu(self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        self.setMenuBar(self.menu_bar)

        self.action_exit = QtGui.QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_about = QtGui.QAction(self)
        self.action_about.setObjectName("action_about")

        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        #======================== Menu Bar Connection ========================
        self.action_exit.triggered.connect(super().close)

        #QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL("triggered()"), super().close)
        #QtCore.QObject.connect(self.action_about, QtCore.SIGNAL("triggered()"), self.about)

        #======================== Statue Bar ========================
        self.status_bar = QtGui.QStatusBar(parent)
        self.setStatusBar(self.status_bar)


        self.banner = QtGui.QLabel(self.centralwidget)
        self.banner.setGeometry(QtCore.QRect(10, 10, 590, 145))
        self.banner.setAlignment(QtCore.Qt.AlignCenter)

        self.table_widget = QtGui.QLabel(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(10, 170, 590, 400))

        self.user_widget = QtGui.QWidget(self.centralwidget)
        self.user_widget.setGeometry(QtCore.QRect(160, 10, 160, 560))

        self.resize(780, 580)
        self.setWindowTitle("uAuction")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(1, DEBUGMODE=True)
    window.show()
    app.exec_()
