__author__ = 'Waterstrider'
import sys

from PyQt5 import QtCore
from PyQt5 import QtQuick
from PyQt5 import QtWidgets
from chimera.auctionListModel import AuctionListModel
from chimera.auctionWrapper import AuctionWrapper
from chimera.Auction import Auction

class ThingWrapper(QtCore.QObject):
    def __init__(self, thing):
        QtCore.QObject.__init__(self)
        self._thing = thing

    def name(self):
        return str(self._thing)

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(str, name, notify=changed)


class ThingListModel(QtCore.QAbstractListModel):
    COLUMNS = ('thing',)

    def __init__(self, things):
        QtCore.QAbstractListModel.__init__(self)
        self._things = things

    def roleNames(self):
        return dict(enumerate(ThingListModel.COLUMNS))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._things)

    def data(self, index, role):
        if index.isValid() and role == ThingListModel.COLUMNS.index('thing'):
            return self._things[index.row()]
        return None


class Controller(QtCore.QObject):
    @QtCore.pyqtSlot(QtCore.QObject)
    def thingSelected(self, wrapper):
        print('User clicked on:', wrapper._thing.name)
        if wrapper._thing.number > 10:
            print('The number is greater than ten!')


class Person(object):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __repr__(self):
        return 'Person "%s" (%d)'%(self.name, self.number)


class Link(QtCore.QObject):
    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot('QString')
    def debug(self, s):
        print(s)


if __name__ == '__main__':
    # Create main app
    myApp = QtWidgets.QApplication(sys.argv)
    # Create a label and set its properties
    view = QtQuick.QQuickView()
    view.setSource(QtCore.QUrl('mainwindow.qml'))
    rc = view.rootContext()
    people = [
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),
        Auction('Locke', 4, 4, 4, 4, 4, 4, 'C:/Users/Waterstrider/PycharmProjects/uAuction/resources\img/noimage.png',4, 4),

        # Person('Locke', 4),
        # Person('Reyes', 8),
        # Person('Ford', 15),
        # Person('Jarrah', 16),
        # Person('Shephard', 23),
        # Person('Kwon', 42),
    ]
    auctions = [AuctionWrapper(auction) for auction in people]
    auctions1 = auctions[:5]
    auctions2 = auctions[5:]
    # link = Link()
    controller = AuctionController()
    thingList1 = AuctionListModel(auctions1)
    thingList2 = AuctionListModel(auctions2)

    rc.setContextProperty('controller', controller)
    rc.setContextProperty('pythonListModel1', thingList1)
    rc.setContextProperty('pythonListModel2', thingList2)
    # rc.setContextProperty('link', link)
    # Show the Label
    view.show()

    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()