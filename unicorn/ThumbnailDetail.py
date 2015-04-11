__author__ = 'Shiraga-P'

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtUiTools

from unicorn.Item import Item
from unicorn.ViewItem import ViewItemDialog


class ThumbnailDetailWidget(QtGui.QWidget):
    def __init__(self, user_id, item_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.item_id = item_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.item = Item(item_id)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\thumbnaildetail.ui')

        self.label_thumbnail = form.findChild(QtGui.QLabel, 'label_thumbnail')
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
        self.label_itemname.setText(self.item.itemname)
        self.label_buyoutprice.setText(str(self.item.buyoutprice))
        self.label_bidprice.setText(str(self.item.bidprice))

        width = self.label_thumbnail.width()
        height = self.label_thumbnail.height()
        self.label_thumbnail.setPixmap(
            QtGui.QPixmap(self.item.thumbnailpath).scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def mouseDoubleClickEvent(self, event):
        viewItemDialog = ViewItemDialog(self.user_id, self.item_id, self.parent)
        viewItemDialog.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = ThumbnailDetailWidget(1, 1, DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())