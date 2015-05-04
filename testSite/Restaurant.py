__author__ = 'Chatchaya'

from PyQt5.QtCore import *
from QObjectListModel import *

class Restaurant(QObject):
    def __init__(self, parent, name, desc, path):
        super(Restaurant, self).__init__(parent)
        self._name = name
        self._desc = desc
        self._path = path

    def getName(self):
        return self._name

    def getDesc(self):
        return self._desc

    def getPath(self):
        return self._path

    nameChanged = pyqtSignal()
    descChanged = pyqtSignal()
    pathChanged = pyqtSignal()
    name = pyqtProperty(str, getName, notify=nameChanged)
    desc = pyqtProperty(str, getDesc, notify=descChanged)
    path = pyqtProperty(str, getPath, notify=pathChanged)

class MainWrapper(QObject):
    def __init__(self, parent, dataList=[]):
        super(MainWrapper, self).__init__(parent)
        self._qtParent = parent
        self._restaurants = QObjectListModel(self)
        self._restaurants.setObjectList(dataList)

    def getRestaurants(self):
        return self._restaurants

    @pyqtSlot(int)
    def remove(self, index):
        self._restaurants.removeAt(index)

    @pyqtSlot()
    def add(self):
        self._restaurants.append(Restaurant(self._qtParent, "RestaurantDynamic", "", "images/18.jpg") )

    @pyqtSlot(int)
    def insertAt(self, index):
        self._restaurants.insert(index, Restaurant(self._qtParent, "RestaurantDynamic", "", "") )

    modelChanged = pyqtSignal()
    restaurants = pyqtProperty(QObject, getRestaurants, notify=modelChanged)
