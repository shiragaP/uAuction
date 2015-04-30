__author__ = 'Waterstrider'
from PyQt5 import QtCore
class AuctionController(QtCore.QObject):
    @QtCore.pyqtSlot(QtCore.QObject)
    def auctionSelected(self, wrapper):
        print('User clicked on:', wrapper.auction.name)