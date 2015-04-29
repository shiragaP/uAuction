__author__ = 'Shiraga-P'

import sys
from datetime import datetime

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtQuick

from chimera.Auctions import Auctions
from chimera.Users import Users


class ViewAuctionDialog(QtWidgets.QDialog):
    def __init__(self, user_id=1, auction_id=1, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.auction_id = auction_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        self.auction = Auctions().getAuction(self.auction_id)
        self.seller = Users().getUser(self.auction.seller_id)

        form = uic.loadUi('ui\\viewauction.ui')

        self.label_name = form.findChild(QtWidgets.QLabel, 'label_00_name')
        self.label_timeleft = form.findChild(QtWidgets.QLabel, 'label_00_timeleft')
        self.label_buyoutprice = form.findChild(QtWidgets.QLabel, 'label_02_buyoutprice')
        self.label_bidprice = form.findChild(QtWidgets.QLabel, 'label_03_bidprice')
        self.label_seller = form.findChild(QtWidgets.QLabel, 'label_04_seller')

        self.textEdit_description = form.findChild(QtWidgets.QTextEdit, 'textEdit_05_description')
        self.textEdit_description.setReadOnly(True)

        self.lineEdit_bidprice = form.findChild(QtWidgets.QLineEdit, 'lineEdit_bidprice')
        self.lineEdit_bidprice.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{0,28}"), self))

        self.pushButton_bid = form.findChild(QtWidgets.QPushButton, 'pushButton_01_bid')
        self.pushButton_buyitnow = form.findChild(QtWidgets.QPushButton, 'pushButton_02_buyitnow')

        self.widget_qquickview = form.findChild(QtWidgets.QWidget, 'widget_qquickview')

        self.view = QtQuick.QQuickView()

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        con = QtWidgets.QWidget.createWindowContainer(self.view, self)
        layout.addWidget(con)
        self.widget_qquickview.setLayout(layout)

        self.pushButton_bid.clicked.connect(self.bidActionListener)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width())
        self.setFixedHeight(form.height())
        self.setWindowTitle('View Auction')

        self.loadAuction()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.reloadTimeLeft)
        self.timer.start(200)

    def loadAuction(self):
        self.auction = Auctions().getAuction(self.auction_id)
        self.label_name.setText(self.auction.name)
        self.label_buyoutprice.setText(str(self.auction.buyoutprice if self.auction.buyoutprice != 0 else '-'))
        self.label_bidprice.setText(str(self.auction.bidprice))
        self.label_seller.setText(self.seller.username)

        self.view.setSource(QtCore.QUrl('viewAuctionImage.qml'))
        rc = self.view.rootContext()
        rc.setContextProperty('pythonListModel', self.auction.imagepaths)
        # class Link(QtCore.QObject):
        # def __init__(self):
        # super().__init__()
        #     # @QtCore.pyqtSlot(int)
        #     @QtCore.pyqtSlot('QString')
        #     def debug(self, s):
        #         print(s)
        # link = Link()
        # rc.setContextProperty('link',link)

        #TODO: load images
        for imagepath in self.auction.imagepaths:
            print(imagepath)

        self.textEdit_description.setText(self.auction.description)

    def bidActionListener(self):
        if self.lineEdit_bidprice.text() == "":
            QtWidgets.QMessageBox.warning(self, "Invalid Bid", "Please enter the bid price.")
            return
        self.loadAuction()
        newBidPrice = self.lineEdit_bidprice.text()
        if int(newBidPrice) > int(self.auction.bidprice):
            Auctions().updateBidPrice(self.auction_id, newBidPrice)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Invalid bid price.")
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
    app = QtWidgets.QApplication(sys.argv)
    viewItemWidget = ViewAuctionDialog(auction_id=1, DEBUGMODE=True)
    viewItemWidget.show()
    sys.exit(app.exec_())