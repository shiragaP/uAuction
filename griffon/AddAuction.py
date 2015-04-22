__author__ = 'Shiraga-P'

import sys
from datetime import datetime, timedelta

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic

from griffon.Auctions import Auctions
from griffon.Auction import Auction
from griffon.Thumbnail import ThumbnailWidgetItem


class AddAuctionDialog(QtWidgets.QDialog):
    def __init__(self, user_id=1, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        #loader = uic.QUiLoader(self)
        form = uic.loadUi('ui\\addauction.ui')

        self.label_image = form.findChild(QtWidgets.QLabel, 'label_01_image')
        self.listWidget_thumbnail = form.findChild(QtWidgets.QListWidget, 'listWidget_thumbnail')
        self.listWidget_thumbnail.setFlow(QtWidgets.QListWidget.LeftToRight)
        self.listWidget_thumbnail.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget_thumbnail.itemSelectionChanged.connect(self.itemSelectionChangedListener)

        self.lineEdit_name = form.findChild(QtWidgets.QLineEdit, 'lineEdit_02_name')
        self.lineEdit_buyoutprice = form.findChild(QtWidgets.QLineEdit, 'lineEdit_03_buyoutprice')
        self.lineEdit_buyoutprice.setReadOnly(True)
        self.lineEdit_bidprice = form.findChild(QtWidgets.QLineEdit, 'lineEdit_04_bidprice')
        self.lineEdit_categories = form.findChild(QtWidgets.QLineEdit, 'lineEdit_05_categories')

        self.checkBox_buyoutavailable = form.findChild(QtWidgets.QCheckBox, 'checkBox_buyoutavailable')
        self.checkBox_buyoutavailable.setChecked(False)
        self.checkBox_buyoutavailable.stateChanged.connect(self.checkBoxActionListener)

        self.textEdit_description = form.findChild(QtWidgets.QTextEdit, 'textEdit_06_description')

        self.pushButton_addimage = form.findChild(QtWidgets.QPushButton, 'pushButton_01_addimage')
        self.pushButton_addimage.clicked.connect(self.addImageActionListener)
        self.pushButton_deleteimage = form.findChild(QtWidgets.QPushButton, 'pushButton_02_deleteimage')
        self.pushButton_deleteimage.clicked.connect(self.deleteImageActionListener)
        self.pushButton_sell = form.findChild(QtWidgets.QPushButton, 'pushButton_03_sell')
        self.pushButton_sell.clicked.connect(self.sellActionListener)
        self.pushButton_cancel = form.findChild(QtWidgets.QPushButton, 'pushButton_04_cancel')
        self.pushButton_cancel.clicked.connect(self.cancelActionListener)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Add Auction')
        self.setAcceptDrops(True)

    def checkBoxActionListener(self):
        if self.checkBox_buyoutavailable.isChecked():
            self.lineEdit_buyoutprice.setReadOnly(False)
        else:
            self.lineEdit_buyoutprice.setReadOnly(True)

    def addImageActionListener(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filepath != '':
            self.addImage(filepath)

    def addImage(self, filepath):
        widgetiItem = ThumbnailWidgetItem(filepath, 60, 60)
        self.listWidget_thumbnail.addItem(widgetiItem)
        self.listWidget_thumbnail.setItemWidget(widgetiItem, widgetiItem.thumbnailWidget)

    def deleteImageActionListener(self):
        items = self.listWidget_thumbnail.selectedItems()
        for item in items:
            self.listWidget_thumbnail.takeItem(self.listWidget_thumbnail.row(item))

    def sellActionListener(self):
        name = self.lineEdit_name.text()
        buyoutavailable = self.checkBox_buyoutavailable.isChecked()
        if buyoutavailable:
            buyoutprice = self.lineEdit_buyoutprice.text()
        else:
            buyoutprice = 0
        seller_id = self.user_id
        bidprice = self.lineEdit_bidprice.text()
        bidnumber = 0
        # TODO: categories
        categories = self.lineEdit_categories.text()
        description = self.textEdit_description.toHtml()

        if self.listWidget_thumbnail.count() == 0:
            thumbnailpath = '..\\resources\\img\\noimage.png'
        else:
            thumbnailpath = self.listWidget_thumbnail.item(0).filepath

        expirytime = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now() + timedelta(days=0))
        soldout = False
        imagepaths = [open(self.listWidget_thumbnail.item(i).filepath) for i in
                      range(self.listWidget_thumbnail.count())]

        try:
            self.addAuction(name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description,
                            thumbnailpath,
                            expirytime, soldout, imagepaths)

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Warning", "Invalid input.")

    def cancelActionListener(self):
        self.close()

    def addAuction(self, name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                   expirytime, soldout, imagepaths):

        Auctions.addAuction(
            Auction(name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                    expirytime, soldout, imagepaths))

        QtWidgets.QMessageBox.information(self, "Notification", "Add item complete!")

        if self.parent:
            self.parent.loadRecentItems()

        self.close()

    # def addAuction(self, name, seller, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnail,
    # expirytime, soldout):
    # conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
    # % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    #     cur = conn.cursor()
    #
    #     statement = """INSERT INTO auctions (name, seller, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnail, expirytime, soldout)
    #                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    #                     """
    #
    #     if (self.DEBUGMODE):
    #         print("Sql Statement")
    #         print(statement)
    #
    #     cur.execute(statement, (name,
    #                             seller,
    #                             buyoutavailable,
    #                             buyoutprice,
    #                             bidprice,
    #                             bidnumber,
    #                             description,
    #                             thumbnail,
    #                             expirytime,
    #                             soldout,))
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #
    #     self.addAuctionImages()
    #
    #     QtWidgets.QMessageBox.information(self, "Notification", "Add item complete!")
    #
    #     if self.parent:
    #         self.parent.loadRecentItems()
    #
    #     self.close()
    #
    # def addAuctionImages(self):
    #     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
    #                             % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    #     cur = conn.cursor()
    #
    #     cur.execute("SELECT max(id) from auctions")
    #     auction_id = cur.fetchall()[0][0]
    #
    #     for i in range(self.listWidget_thumbnail.count()):
    #         item = self.listWidget_thumbnail.item(i)
    #
    #         statement = """INSERT INTO auction_images (directory, auctionid)
    #                         VALUES (%s, %s);
    #                         """
    #
    #         if (self.DEBUGMODE):
    #             print("Sql Statement")
    #             print(statement)
    #
    #         cur.execute(statement, (item.filepath,
    #                                 auction_id,))
    #
    #     conn.commit()
    #     cur.close()
    #     conn.close()

    def itemSelectionChangedListener(self):
        if len(self.listWidget_thumbnail.selectedItems()) > 0:
            pixmap = QtWidgets.QPixmap(self.listWidget_thumbnail.selectedItems()[0].thumbnailImage)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.size(), QtCore.Qt.KeepAspectRatio))

    def dragEnterEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def imageFileFilter(self, droppedUrls):
        droppedUrlCnt = len(droppedUrls)
        for i in range(droppedUrlCnt):
            localPath = droppedUrls[i].toLocalFile()
            fileInfo = QtCore.QFileInfo(localPath)
            if (fileInfo.isFile()):
                # file
                if fileInfo.suffix() in ["png", "jpg"]:
                    QtWidgets.QMessageBox.information(self, self.tr("Dropped image file"), fileInfo.absoluteFilePath())
                    self.addImage(fileInfo.absoluteFilePath())
                else:
                    QtWidgets.QMessageBox.information(self, self.tr("Dropped file"), fileInfo.absoluteFilePath())
            elif (fileInfo.isDir()):
                # directory
                it = QtCore.QDirIterator(fileInfo.absoluteFilePath(), ("*.png", "*.jpg"), QtCore.QDir.Files,
                    QtCore.QDirIterator.Subdirectories)
                while it.hasNext():
                    self.addImage(it.next())
                QtWidgets.QMessageBox.information(self, self.tr("Dropped directory"), fileInfo.absoluteFilePath())
            else:
                # none
                QtWidgets.QMessageBox.information(self, self.tr("Dropped, but unknown"),
                                              self.tr("Unknown: %1").arg(fileInfo.absoluteFilePath()))

    def dropEvent(self, event):
        droppedUrls = event.mimeData().urls()
        self.imageFileFilter(droppedUrls)
        event.acceptProposedAction()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    addAuctionDialog = AddAuctionDialog(DEBUGMODE=True)
    addAuctionDialog.show()
    sys.exit(app.exec_())