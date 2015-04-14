__author__ = 'Shiraga-P'

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtUiTools

from griffon.Auctions import Auctions
from griffon.ViewAuction import ViewAuctionDialog


class ThumbnailDetailWidget(QtGui.QWidget):
    def __init__(self, user_id, auction_id, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.auction_id = auction_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.auction = Auctions.getAuction(self.auction_id)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\thumbnaildetail.ui')

        self.label_thumbnail = form.findChild(QtGui.QLabel, 'label_thumbnail')
        self.label_name = form.findChild(QtGui.QLabel, 'label_name')
        self.label_buyoutprice = form.findChild(QtGui.QLabel, 'label_buyoutprice')
        self.label_bidprice = form.findChild(QtGui.QLabel, 'label_bidprice')

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Thumbnail')

        self.loadAuction()

    def loadAuction(self):
        self.label_name.setText(self.auction.name)
        self.label_buyoutprice.setText(str(self.auction.buyoutprice))
        self.label_bidprice.setText(str(self.auction.bidprice))

        width = self.label_thumbnail.width()
        height = self.label_thumbnail.height()
        self.label_thumbnail.setPixmap(
            QtGui.QPixmap(self.auction.thumbnailpath).scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def mouseDoubleClickEvent(self, event):
        viewAuctionDialog = ViewAuctionDialog(self.user_id, self.auction_id, self.parent)
        viewAuctionDialog.exec_()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = ThumbnailDetailWidget(1, 1, DEBUGMODE=True)
    loginWidget.show()
    sys.exit(app.exec_())