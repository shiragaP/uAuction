__author__ = 'Waterstrider'

from PyQt5 import QtCore

class AuctionWrapper(QtCore.QObject):
    def __init__(self, auction, buyer):
        QtCore.QObject.__init__(self)
        self.auction = auction
        self.buyer = buyer

    def auction_id(self):
        return str(self.auction.auction_id)

    def name(self):
        return str(self.auction.name)

    def buyoutprice(self):
        return str(self.auction.buyoutprice)

    def bidprice(self):
        return str(self.auction.bidprice)

    def thumbnailpath(self):
        return str(self.auction.thumbnailpath)

    def buyer(self):
        return str(self.auction.buyer)

    namechanged = QtCore.pyqtSignal()
    buyoutpricechanged = QtCore.pyqtSignal()
    bidpricechanged = QtCore.pyqtSignal()
    thumbnailpathchanged = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(str, name, notify=namechanged)
    buyoutprice = QtCore.pyqtProperty(str, buyoutprice, notify=buyoutpricechanged)
    bidprice = QtCore.pyqtProperty(str, bidprice, notify=bidpricechanged)
    thumbnailpath = QtCore.pyqtProperty(str, thumbnailpath, notify=thumbnailpathchanged)

