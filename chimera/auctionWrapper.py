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

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(str, name, notify=changed)
    buyoutprice = QtCore.pyqtProperty(str, buyoutprice, notify=changed)
    bidprice = QtCore.pyqtProperty(str, bidprice, notify=changed)
    thumbnailpath = QtCore.pyqtProperty(str, thumbnailpath, notify=changed)

