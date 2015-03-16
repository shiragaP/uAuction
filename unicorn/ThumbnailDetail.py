__author__ = 'Shiraga-P'

import sys

import psycopg2
from PySide import QtGui
from PySide import QtUiTools

import DatabaseInfo


class ThumbnailDetailWidget(QtGui.QWidget):
    def __init__(self, item_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.item_id = item_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\thumbnaildetail.ui')

        self.label_thunbnail = form.findChild(QtGui.QLabel, 'label_thunbnail')
        self.label_itemname = form.findChild(QtGui.QLabel, 'label_itemname')
        self.label_buyoutprice = form.findChild(QtGui.QLabel, 'label_buyoutprice')
        self.label_bidprice = form.findChild(QtGui.QLabel, 'label_bidprice')

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Thumbnail')

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

        self.label_thunbnail.setPixmap(QtGui.QPixmap(self.thumbnail))
        self.label_name.setText(str(self.buyoutprice))
        self.label_buyoutprice.setText(str(self.buyoutprice))
        self.label_bidprice.setText(str(self.bidprice))

        self.textEdit_description.setText(self.description)

        conn.commit()
        cur.close()
        conn.close()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = ThumbnailDetailWidget(1, DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())