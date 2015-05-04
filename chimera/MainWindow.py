import sys, re

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtQuick

from threading import Timer

from chimera.AddAuction import AddAuctionDialog
from chimera.ViewAuction import ViewAuctionDialog
from chimera.Auctions import Auctions
from chimera.Users import Users
from chimera.Register import RegisterDialog
from chimera.auctionListModel import AuctionListModel
from chimera.auctionWrapper import AuctionWrapper


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id=0, parent=None, DEBUGMODE=False):
        super().__init__(parent) #, QtCore.Qt.FramelessWindowHint)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        form = uic.loadUi('ui\\mainwindow.ui')

        self.label_logo = form.findChild(QtWidgets.QWidget, 'label_logo')
        self.label_logo.setPixmap(QtGui.QPixmap("..\\resources\\img\\logo.png").scaled(self.label_logo.size(), QtCore.Qt.KeepAspectRatio))

        self.lineEdit_search = form.findChild(QtWidgets.QLineEdit, 'lineEdit_search')
        self.pushButton_search = form.findChild(QtWidgets.QPushButton, 'pushButton_search')
        self.pushButton_search.clicked.connect(self.searchClickedActionListener)

        self.pushButton_next = form.findChild(QtWidgets.QPushButton, 'pushButton_next')
        self.pushButton_next.clicked.connect(self.nextClickedActionListener)
        self.pushButton_p1 = form.findChild(QtWidgets.QPushButton, 'pushButton_p1')
        self.pushButton_p2 = form.findChild(QtWidgets.QPushButton, 'pushButton_p2')
        self.pushButton_p3 = form.findChild(QtWidgets.QPushButton, 'pushButton_p3')
        self.pushButton_p4 = form.findChild(QtWidgets.QPushButton, 'pushButton_p4')
        self.pushButton_p5 = form.findChild(QtWidgets.QPushButton, 'pushButton_p5')
        self.pushButton_prev = form.findChild(QtWidgets.QPushButton, 'pushButton_prev')
        self.pushButton_prev.clicked.connect(self.prevClickedActionListener)

        self.label_cat = list()
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_1'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_2'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_3'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_4'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_5'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_6'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_7'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_8'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_9'))
        self.label_cat.append(form.findChild(QtWidgets.QLabel, 'label_cat_10'))

        self.widget_login = form.findChild(QtWidgets.QWidget, 'widget_login')
        self.lineEdit_user = form.findChild(QtWidgets.QLineEdit, 'lineEdit_user')
        self.lineEdit_user.returnPressed.connect(self.loginClickedActionListener)
        self.lineEdit_pass = form.findChild(QtWidgets.QLineEdit, 'lineEdit_pass')
        self.lineEdit_pass.returnPressed.connect(self.loginClickedActionListener)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton_login = form.findChild(QtWidgets.QPushButton, 'pushButton_login')
        self.pushButton_login.clicked.connect(self.loginClickedActionListener)
        self.pushButton_register = form.findChild(QtWidgets.QPushButton, 'pushButton_register')
        self.pushButton_register.clicked.connect(self.registerClickedActionListener)

        self.widget_info = form.findChild(QtWidgets.QWidget, 'widget_info')
        self.label_name = form.findChild(QtWidgets.QLabel, 'label_name')
        self.label_user = form.findChild(QtWidgets.QLabel, 'label_user')
        self.label_userid = form.findChild(QtWidgets.QLabel, 'label_userid')

        self.pushButton_sell = form.findChild(QtWidgets.QPushButton, 'pushButton_sell')
        self.pushButton_sell.clicked.connect(self.sellClickedActionListener)
        self.pushButton_seeprofile = form.findChild(QtWidgets.QPushButton, 'pushButton_seeprofile')
        self.pushButton_seebidhistory = form.findChild(QtWidgets.QPushButton, 'pushButton_seebidhistory')
        self.pushButton_seebidhistory.clicked.connect(self.seebidhistoryClickedActionListener)
        self.pushButton_logout = form.findChild(QtWidgets.QPushButton, 'pushButton_logout')
        self.pushButton_logout.clicked.connect(self.logoutClickedActionListener)

        self.widget_qquickview = form.findChild(QtWidgets.QWidget, 'widget_qquickview')
        self.view = QtQuick.QQuickView()
        self.view.setSource(QtCore.QUrl('ui/mainwindow.qml'))
        self.rootContext = self.view.rootContext()
        self.rootContext.setContextProperty('controller', self)
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        con = QtWidgets.QWidget.createWindowContainer(self.view, self)
        layout.addWidget(con)
        self.widget_qquickview.setLayout(layout)

        self.setCentralWidget(form)

        self.setMinimumSize(form.size())
        self.setMaximumSize(form.size())
        self.setWindowIcon(QtGui.QIcon('..\\resources\\img\\icon.png'))
        self.setWindowTitle("uAuction")

        self.auctionList1 = AuctionListModel(self)
        self.auctionList2 = AuctionListModel(self)
        self.rootContext.setContextProperty('pythonListModel1', self.auctionList1)
        self.rootContext.setContextProperty('pythonListModel2', self.auctionList2)
        self.currentPage = 1

        self.loadRecentAuction()
        self.showGuestWidgets()
        self.loadPopularCategories()

    def loadRecentAuction(self):
        self.currentPage = 1
        self.auctionList = Auctions().getActiveAuctionIDs()
        self.loadItemsFromRight()

    def loadItemsFromRight(self):
        print(self.auctionList)

        auctionIDsToLoad = self.auctionList[(self.currentPage-1)*10: (self.currentPage-1)*10+10]
        auctionList = Auctions()
        self.currentAuctionWrappers = list()
        for auctionid in auctionIDsToLoad:
            self.currentAuctionWrappers.append(AuctionWrapper(auctionList.getAuction(auctionid[0]), self.user_id))
        auctions1 = self.currentAuctionWrappers[:5]
        auctions2 = self.currentAuctionWrappers[5:]
        self.auctionList1.clearAuctions()
        self.auctionList2.clearAuctions()
        for auction in auctions1:
            self.auctionList1._auctions.append(auction)
        for auction in auctions2:
            self.auctionList2._auctions.append(auction)

    def loadItemsFromRightThread(self):
        auctionIDsToLoad = self.auctionList[(self.currentPage-1)*10: (self.currentPage-1)*10+10]
        auctionList = Auctions()
        self.currentAuctionWrappers = list()
        for auctionid in auctionIDsToLoad:
            self.currentAuctionWrappers.append(AuctionWrapper(auctionList.getAuction(auctionid[0]), self.user_id))
        auctions1 = self.currentAuctionWrappers[:5]
        auctions2 = self.currentAuctionWrappers[5:]
        self.auctionList1.clearAuctions()
        self.auctionList2.clearAuctions()
        for auction in auctions1:
            self.auctionList1._auctions.append(auction)
        for auction in auctions2:
            self.auctionList2._auctions.append(auction)
        print(self.auctionList1.getAuctions())

    def searchClickedActionListener(self):
        keywords = list(filter(''.__ne__, re.split(" |,|#", self.lineEdit_search.text())))
        if len(keywords) < 1:
            self.loadRecentAuction()
        else:
            self.auctionList = Auctions().searchAuctionIDs(keywords)
            self.currentPage = 1
            self.loadItemsFromRight()

    def nextClickedActionListener(self):
        if self.currentPage < len(self.auctionList) / 10:
            self.currentPage += 1
        self.loadItemsFromRight()

    def prevClickedActionListener(self):
        if self.currentPage > 1:
            self.currentPage -= 1
        self.loadItemsFromRight()

    def loginClickedActionListener(self):
        if self.lineEdit_user.text() == "" or self.lineEdit_pass.text() =="":
            QtWidgets.QMessageBox.warning(self, "Invalid Login", "Please enter the username and the password.")
            return
        self.user_id = Users().validUser(self.lineEdit_user.text(), self.lineEdit_pass.text())
        if self.user_id > 0:
            self.login(Users().getUser(self.user_id))
        else:
            self.user_id = 0
            self.showGuestWidgets()

    def login(self, user):
        self.label_name.setText(user.firstname)
        self.label_user.setText(user.username)
        self.label_userid.setText("(" + ("%04d" % user.user_id) + ")")
        self.showUserWidgets()

        for wrapper in self.currentAuctionWrappers:
            wrapper.buyer = self.user_id

    def registerClickedActionListener(self):
        registerDialog = RegisterDialog(DEBUGMODE=self.DEBUGMODE)
        registerDialog.exec_()

    def sellClickedActionListener(self):
        addAuctionDialog = AddAuctionDialog(DEBUGMODE=self.DEBUGMODE)
        addAuctionDialog.exec_()

    def seebidhistoryClickedActionListener(self):
        self.auctionList = Auctions().getBidHistory(self.user_id)
        self.currentPage = 1
        self.loadItemsFromRight()

    def logoutClickedActionListener(self):
        self.user_id = 0
        self.showGuestWidgets()

        for wrapper in self.currentAuctionWrappers:
            wrapper.buyer = self.user_id

    def showGuestWidgets(self):
        self.lineEdit_user.setText('')
        self.lineEdit_pass.setText('')

        self.widget_info.hide()
        self.pushButton_sell.hide()
        self.pushButton_seeprofile.hide()
        self.pushButton_seebidhistory.hide()
        self.pushButton_logout.hide()

        self.widget_login.show()
        self.pushButton_login.show()
        self.pushButton_register.show()

    def showUserWidgets(self):
        self.widget_login.hide()
        self.pushButton_login.hide()
        self.pushButton_register.hide()

        self.widget_info.show()
        self.pushButton_sell.show()
        self.pushButton_seeprofile.show()
        self.pushButton_seebidhistory.show()
        self.pushButton_logout.show()

    def loadPopularCategories(self):
        categories = Auctions().getPopularCategories()
        for i in range(len(categories)):
            self.label_cat[i].setText(categories[i][0])

    @QtCore.pyqtSlot(QtCore.QObject)
    def auctionSelected(self, wrapper):
        if wrapper.getbuyer == 0:
            QtWidgets.QMessageBox.warning(self, "Authentication Failed", "Please login to view auction details", )
        else:
            viewAuctionDialog = ViewAuctionDialog(user_id=self.user_id, auction_id=wrapper.auction.auction_id, DEBUGMODE=self.DEBUGMODE)
            viewAuctionDialog.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(DEBUGMODE=True)
    window.show()
    app.exec_()
