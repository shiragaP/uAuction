__author__ = 'Waterstrider'

from PyQt5 import QtCore

class AuctionWrapper(QtCore.QObject):
    def __init__(self, auction, buyer):
        QtCore.QObject.__init__(self)
        self._auction = auction
        self._buyer = buyer

    def getauction_id(self):
        return str(self.auction.auction_id)

    def getname(self):
        return str(self.auction.name)

    def getbuyoutprice(self):
        return str(self.auction.buyoutprice)

    def getbidprice(self):
        return str(self.auction.bidprice)

    def getthumbnailpath(self):
        return str(self.auction.thumbnailpath)

    def getbuyer(self):
        return str(self.auction.buyer)

    namechanged = QtCore.pyqtSignal()
    buyoutpricechanged = QtCore.pyqtSignal()
    bidpricechanged = QtCore.pyqtSignal()
    thumbnailpathchanged = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(str, getname, notify=namechanged)
    buyoutprice = QtCore.pyqtProperty(str, getbuyoutprice, notify=buyoutpricechanged)
    bidprice = QtCore.pyqtProperty(str, getbidprice, notify=bidpricechanged)
    thumbnailpath = QtCore.pyqtProperty(str, getthumbnailpath, notify=thumbnailpathchanged)

