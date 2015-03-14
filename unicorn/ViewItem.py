__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from PySide import QtGui, QtCore
from PySide import QtUiTools


class AddItemDialog(QtGui.QDialog):

    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\viewitem.ui')

        self.label_itemname = form.findChild(QtGui.QLabel, 'label_00_itemname')
        self.label_image = form.findChild(QtGui.QLabel, 'label_01_image')
        self.label_buyoutprice = form.findChild(QtGui.QLabel, 'label_02_buyoutprice')
        self.label_bidprice = form.findChild(QtGui.QLabel, 'label_03_bidprice')

        self.listWidget_thunbnail = form.findChild(QtGui.QListWidget, 'listWidget_thunbnail')

        self.textEdit_description = form.findChild(QtGui.QTextEdit, 'textEdit_04_description')
        self.textEdit_description.setReadOnly(True)

        self.lineEdit_bidprice = form.findChild(QtGui.QLineEdit, 'lineEdit_bidprice')

        self.pushButton_bid = form.findChild(QtGui.QPushButton, 'pushButton_01_bid')
        self.pushButton_buyitnow = form.findChild(QtGui.QPushButton, 'pushButton_02_buyitnow')

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Add Item')




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    addItemWidget = AddItemDialog(DEBUGMODE=True)
    addItemWidget.show()
    sys.exit(app.exec_())