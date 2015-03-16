__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from PySide import QtGui, QtCore
from PySide import QtUiTools


class ViewItemDialog(QtGui.QDialog):

    def __init__(self, user_id, item_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.item_id = item_id
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
        self.setWindowTitle('View Item')

        self.loadItem()

    def loadItem(self):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from items WHERE items.id=%s", (self.item_id,))

        row = cur.fetchall()[0]

        self.itemname = row[1]
        self.seller_id = row[2]
        self.buyoutavailable = row[3]
        self.buyoutprice = row[4]
        self.bidprice = row[5]
        self.bidnumber = row[6]
        self.description = row[7]
        self.thumbnail = row[8]

        self.loadImages()
        self.loadSeller()

        self.label_itemname.setText(self.itemname)
        self.label_image.setPixmap(QtGui.QPixmap(self.thumbnail))
        self.label_buyoutprice.setText(str(self.buyoutprice))
        self.label_bidprice.setText(str(self.bidprice))

        self.textEdit_description.setText(self.description)

        conn.commit()
        cur.close()
        conn.close()

    def loadImages(self):
        pass

    def loadSeller(self):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from items WHERE items.id=%s", (self.item_id,))

        row = cur.fetchall()[0]

        self.seller_username = row[1]

        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    addItemWidget = ViewItemDialog(1, 8, DEBUGMODE=True)
    addItemWidget.show()
    sys.exit(app.exec_())