__author__ = 'Shiraga-P'

import sys
from datetime import datetime

from PySide import QtCore
from PySide import QtGui
from PySide import QtUiTools

from griffon.Auctions import Auctions
from griffon.Thumbnail import ThumbnailWidgetItem
from griffon.User import User


class ViewAuctionDialog(QtGui.QDialog):
    def __init__(self, user_id=1, auction_id=1, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.auction_id = auction_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.auction = Auctions.getAuction(self.auction_id)
        self.seller = User(self.auction.seller_id)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\viewauction.ui')

        self.label_name = form.findChild(QtGui.QLabel, 'label_00_name')
        self.label_timeleft = form.findChild(QtGui.QLabel, 'label_00_timeleft')
        self.label_image = form.findChild(QtGui.QLabel, 'label_01_image')
        self.label_buyoutprice = form.findChild(QtGui.QLabel, 'label_02_buyoutprice')
        self.label_bidprice = form.findChild(QtGui.QLabel, 'label_03_bidprice')
        self.label_seller = form.findChild(QtGui.QLabel, 'label_04_seller')

        self.listWidget_thumbnail = form.findChild(QtGui.QListWidget, 'listWidget_thumbnail')
        self.listWidget_thumbnail.setFlow(QtGui.QListWidget.LeftToRight)
        self.listWidget_thumbnail.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget_thumbnail.itemSelectionChanged.connect(self.itemSelectionChangedListener)

        self.textEdit_description = form.findChild(QtGui.QTextEdit, 'textEdit_05_description')
        self.textEdit_description.setReadOnly(True)

        self.lineEdit_bidprice = form.findChild(QtGui.QLineEdit, 'lineEdit_bidprice')
        self.lineEdit_bidprice.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{0,28}"), self))

        self.pushButton_bid = form.findChild(QtGui.QPushButton, 'pushButton_01_bid')
        self.pushButton_buyitnow = form.findChild(QtGui.QPushButton, 'pushButton_02_buyitnow')

        self.pushButton_bid.clicked.connect(self.bidActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('View Auction')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.reloadTimeLeft)
        self.timer.start(200)

        self.loadAuction()

    def loadAuction(self):
        self.auction = Auctions.getAuction(self.auction_id)
        self.label_name.setText(self.auction.name)
        self.label_buyoutprice.setText(str(self.auction.buyoutprice if self.auction.buyoutprice != 0 else '-'))
        self.label_bidprice.setText(str(self.auction.bidprice))
        self.label_seller.setText(self.seller.username)

        self.auction.imagepaths[0].seek(0)
        data = self.auction.imagepaths[0].read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        self.label_image.setPixmap(pixmap.scaled(self.label_image.size(), QtCore.Qt.KeepAspectRatio))

        if len(self.auction.imagepaths) > 5:
            thumbnailWidth = thumbnailHeight = 60
        else:
            thumbnailWidth = thumbnailHeight = 75

        self.listWidget_thumbnail.clear()
        for imagepath in self.auction.imagepaths:
            widgetiItem = ThumbnailWidgetItem(imagepath, thumbnailWidth, thumbnailHeight)
            self.listWidget_thumbnail.addItem(widgetiItem)
            self.listWidget_thumbnail.setItemWidget(widgetiItem, widgetiItem.thumbnailWidget)

        self.textEdit_description.setText(self.auction.description)

    def bidActionListener(self):
        self.loadAuction()
        newBidPrice = self.lineEdit_bidprice.text()
        if int(newBidPrice) > int(self.auction.bidprice):
            Auctions.updateBidPrice(self.auction_id, newBidPrice)
            self.loadAuction()

    def reloadTimeLeft(self):
        time_left = self.auction.expirytime - datetime.now()
        time_left = (time_left.days, time_left.seconds // 3600, (time_left.seconds // 60) % 60, time_left.seconds % 60)

        if time_left[0] < 0 or self.auction.soldout == True:
            time_left_str = "END"
        elif time_left[0] > 0:
            time_left_str = "%dd %dhr %dm %ds" % time_left[0:]
        elif time_left[1] > 0:
            time_left_str = "%dhr %dm %ds" % time_left[1:]
        elif time_left[2] > 0:
            time_left_str = "%dm %ds" % time_left[2:]
        elif time_left[3] > 0:
            time_left_str = "%ds" % time_left[3:]
        else:
            time_left_str = "END"

        self.label_timeleft.setText(time_left_str)

    def itemSelectionChangedListener(self):
        if len(self.listWidget_thumbnail.selectedItems()) > 0:
            self.label_image.setPixmap(
                QtGui.QPixmap(self.listWidget_thumbnail.selectedItems()[0].thumbnailImage).scaled(
                    self.label_image.size(), QtCore.Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    addItemWidget = ViewAuctionDialog(auction_id=1, DEBUGMODE=True)
    addItemWidget.show()
    sys.exit(app.exec_())