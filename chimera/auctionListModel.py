__author__ = 'Waterstrider'
from PyQt5 import QtCore
class AuctionListModel(QtCore.QAbstractListModel):
    COLUMNS = ('auction',)

    def __init__(self, auctions):
        QtCore.QAbstractListModel.__init__(self)
        self.auctions = auctions

    def roleNames(self):
        return dict(enumerate(AuctionListModel.COLUMNS))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.auctions)

    def data(self, index, role):
        if index.isValid() and role == AuctionListModel.COLUMNS.index('auction'):
            return self.auctions[index.row()]
        return None