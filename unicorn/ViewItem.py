__author__ = 'Shiraga-P'

import sys

import psycopg2
from PySide import QtGui
from PySide import QtUiTools

from unicorn.Item import Item
from unicorn.User import User
import DatabaseInfo


class ViewItemDialog(QtGui.QDialog):
    def __init__(self, user_id, item_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.item_id = item_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.item = Item(item_id)
        self.seller = User(self.item.seller_id)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\viewitem.ui')

        self.label_itemname = form.findChild(QtGui.QLabel, 'label_00_itemname')
        self.label_image = form.findChild(QtGui.QLabel, 'label_01_image')
        self.label_buyoutprice = form.findChild(QtGui.QLabel, 'label_02_buyoutprice')
        self.label_bidprice = form.findChild(QtGui.QLabel, 'label_03_bidprice')
        self.label_seller = form.findChild(QtGui.QLabel, 'label_04_seller')

        self.listWidget_thunbnail = form.findChild(QtGui.QListWidget, 'listWidget_thunbnail')

        self.textEdit_description = form.findChild(QtGui.QTextEdit, 'textEdit_05_description')
        self.textEdit_description.setReadOnly(True)

        self.lineEdit_bidprice = form.findChild(QtGui.QLineEdit, 'lineEdit_bidprice')

        self.pushButton_bid = form.findChild(QtGui.QPushButton, 'pushButton_01_bid')
        self.pushButton_buyitnow = form.findChild(QtGui.QPushButton, 'pushButton_02_buyitnow')

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('View Item')

        self.loadItem()

    def loadItem(self):
        self.loadSeller()

        self.label_itemname.setText(self.item.itemname)
        self.label_buyoutprice.setText(str(self.item.buyoutprice))
        self.label_bidprice.setText(str(self.item.bidprice))
        self.label_seller.setText(self.seller.username)

        self.label_image.setPixmap(QtGui.QPixmap(self.item.thumbnail))

        self.textEdit_description.setText(self.item.description)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    addItemWidget = ViewItemDialog(1, 8, DEBUGMODE=True)
    addItemWidget.show()
    sys.exit(app.exec_())