__author__ = 'Shiraga-P'

import sys
import psycopg2
import DatabaseInfo

from PySide import QtGui, QtCore
from PySide import QtUiTools


class AddItemDialog(QtGui.QDialog):

    def __init__(self, user_id = 0, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\additem.ui')

        self.label_image = form.findChild(QtGui.QLabel, 'label_01_image')
        self.listWidget_thunbnail = form.findChild(QtGui.QListWidget, 'listWidget_thunbnail')

        self.lineEdit_itemname = form.findChild(QtGui.QLineEdit, 'lineEdit_02_itemname')
        self.lineEdit_buyoutprice = form.findChild(QtGui.QLineEdit, 'lineEdit_03_buyoutprice')
        self.lineEdit_buyoutprice.setReadOnly(True)
        self.lineEdit_bidprice = form.findChild(QtGui.QLineEdit, 'lineEdit_04_bidprice')
        self.lineEdit_categories = form.findChild(QtGui.QLineEdit, 'lineEdit_05_categories')

        self.checkBox_buyoutavailable = form.findChild(QtGui.QCheckBox, 'checkBox_buyoutavailable')
        self.checkBox_buyoutavailable.setChecked(False)
        self.checkBox_buyoutavailable.stateChanged.connect(self.checkBoxActionListener)

        self.textEdit_description = form.findChild(QtGui.QTextEdit, 'textEdit_06_description')

        self.pushButton_addimage = form.findChild(QtGui.QPushButton, 'pushButton_01_addimage')
        self.pushButton_addimage.clicked.connect(self.addImageActionListener)
        self.pushButton_deleteimage = form.findChild(QtGui.QPushButton, 'pushButton_02_deleteimage')
        self.pushButton_addimage.clicked.connect(self.deleteImageActionListener)
        self.pushButton_additem = form.findChild(QtGui.QPushButton, 'pushButton_03_additem')
        self.pushButton_additem.clicked.connect(self.addItemActionListener)
        self.pushButton_cancel = form.findChild(QtGui.QPushButton, 'pushButton_04_cancel')
        self.pushButton_cancel.clicked.connect(self.cancelActionListener)

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)
        self.setWindowTitle('Add Item')

    def checkBoxActionListener(self):
        if self.checkBox_buyoutavailable.isChecked():
            self.lineEdit_buyoutprice.setReadOnly(False)
        else:
            self.lineEdit_buyoutprice.setReadOnly(True)

    def addImageActionListener(self):
        pass

    def deleteImageActionListener(self):
        pass

    def addItemActionListener(self):
        name = self.lineEdit_itemname.text()
        buyoutavailable = self.checkBox_buyoutavailable.isChecked()
        if buyoutavailable:
            buyoutprice = self.lineEdit_buyoutprice.text()
        else:
            buyoutprice = 0
        seller = self.user_id
        bidprice = self.lineEdit_bidprice.text()
        bidnumber = 0
        categories = self.lineEdit_categories.text()
        description = self.textEdit_description.toPlainText()

        thumbnail = '..\\resources\\img\\logo.png' #TODO:

        bidnumber=0

        self.addItem(name, seller, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnail)

    def cancelActionListener(self):
        self.close()

    def addItem(self, name, seller, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnail):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"
                                % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        statement = """INSERT INTO items (name, seller, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnail)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """


        if (self.DEBUGMODE):
            print("Sql Statement")
            print(statement)

        cur.execute(statement, (name,
                               seller,
                               buyoutavailable,
                               buyoutprice,
                               bidprice,
                               bidnumber,
                               description,
                               thumbnail,))
        conn.commit()
        cur.close()
        conn.close()

        QtGui.QMessageBox.information(self, "Notification", "Add item complete!")

        #self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    addItemWidget = AddItemDialog(DEBUGMODE=True)
    addItemWidget.show()
    sys.exit(app.exec_())