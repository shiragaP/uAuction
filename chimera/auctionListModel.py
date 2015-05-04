__author__ = 'Waterstrider'
from PyQt5 import QtCore
from chimera.QObjectListModel import QObjectListModel
# class AuctionListModel(QtCore.QAbstractListModel):
#     COLUMNS = ('auction',)
#
#     def __init__(self, auctions):
#         QtCore.QAbstractListModel.__init__(self)
#         self.auctions = auctions
#
#     def roleNames(self):
#         return dict(enumerate(AuctionListModel.COLUMNS))
#
#     def rowCount(self, parent=QtCore.QModelIndex()):
#         return len(self.auctions)
#
#     def data(self, index, role):
#         if index.isValid() and role == AuctionListModel.COLUMNS.index('auction'):
#             return self.auctions[index.row()]
#         return None

class AuctionListModel(QtCore.QObject):
    def __init__(self, parent, dataList=[]):
        super(AuctionListModel, self).__init__(parent)
        self._qtParent = parent
        self._auctions = QObjectListModel(self)
        self._auctions.setObjectList(dataList)

    def getRestaurants(self):
        return self._restaurants

    modelChanged = QtCore.pyqtSignal()
    restaurants = QtCore.pyqtProperty(QtCore.QObject, getRestaurants, notify=modelChanged)