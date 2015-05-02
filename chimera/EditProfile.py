__author__ = 'Shiraga-P'

import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic

from chimera.Users import Users


class EditProfileDialog(QtWidgets.QDialog):
    def __init__(self, user_id=1, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.user_id = user_id
        self.DEBUGMODE = DEBUGMODE

        self.user = Users().getUser(self.user_id)

        form = uic.loadUi('ui\\editProfile.ui')

        self.lineEdit_username = form.findChild(QtWidgets.QLineEdit, 'lineEdit_01_username')
        self.lineEdit_username.setMaxLength(12)
        self.lineEdit_username.setText(self.user.username)
        self.lineEdit_username.setEnabled(False)
        self.lineEdit_password = form.findChild(QtWidgets.QLineEdit, 'lineEdit_02_password')
        self.lineEdit_password.setMaxLength(12)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setText(self.user.password)
        self.lineEdit_repassword = form.findChild(QtWidgets.QLineEdit, 'lineEdit_03_repassword')
        self.lineEdit_repassword.setMaxLength(12)
        self.lineEdit_repassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_repassword.setText(self.user.password)
        self.lineEdit_email = form.findChild(QtWidgets.QLineEdit, 'lineEdit_04_email')
        self.lineEdit_email.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9@_-+*/]{0,28}"), self))
        self.lineEdit_email.setText(self.user.email)
        self.lineEdit_firstname = form.findChild(QtWidgets.QLineEdit, 'lineEdit_05_firstname')
        self.lineEdit_firstname.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_firstname.setText(self.user.firstname)
        self.lineEdit_lastname = form.findChild(QtWidgets.QLineEdit, 'lineEdit_06_lastname')
        self.lineEdit_lastname.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_lastname.setText(self.user.lastname)
        self.lineEdit_address1 = form.findChild(QtWidgets.QLineEdit, 'lineEdit_07_address1')
        self.lineEdit_address1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9_-+*/]{0,28}"), self))
        self.lineEdit_address1.setText(self.user.address1)
        self.lineEdit_address2 = form.findChild(QtWidgets.QLineEdit, 'lineEdit_08_address2')
        self.lineEdit_address2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9_-+*/]{0,28}"), self))
        self.lineEdit_address2.setText(self.user.address2)
        self.lineEdit_province = form.findChild(QtWidgets.QLineEdit, 'lineEdit_09_province')
        self.lineEdit_province.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_province.setText(self.user.province)
        self.lineEdit_country = form.findChild(QtWidgets.QLineEdit, 'lineEdit_10_country')
        self.lineEdit_country.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]{0,28}"), self))
        self.lineEdit_country.setText(self.user.country)
        self.lineEdit_zipcode = form.findChild(QtWidgets.QLineEdit, 'lineEdit_11_zipcode')
        self.lineEdit_zipcode.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{0,28}"), self))
        self.lineEdit_zipcode.setText(self.user.zipcode)
        self.lineEdit_phonenumber = form.findChild(QtWidgets.QLineEdit, 'lineEdit_12_phonenumber')
        self.lineEdit_phonenumber.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{0,28}"), self))
        self.lineEdit_phonenumber.setText(self.user.phonenumber)

        self.pushButton_editProfile = form.findChild(QtWidgets.QPushButton, 'pushButton_editProfile')
        self.pushButton_editProfile.clicked.connect(self.editProfileActionListener)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width())
        self.setFixedHeight(form.height())
        self.setWindowTitle('Edit Profile')

    def editProfileActionListener(self):
        invalidFlags = list()

        username = self.lineEdit_username.text()
        if 4 > len(username):
            invalidFlags.append('Username')

        password = self.lineEdit_password.text()
        if 4 > len(password):
            invalidFlags.append('Password')
        if 'password' not in invalidFlags and password != self.lineEdit_repassword.text():
            invalidFlags.append('Re-Password')

        email = self.lineEdit_email.text()
        if not email:
            invalidFlags.append('Email')

        firstname = self.lineEdit_firstname.text()
        if not firstname:
            invalidFlags.append('Firstname')

        lastname = self.lineEdit_lastname.text()
        if not lastname:
            invalidFlags.append('Lastname')

        address1 = self.lineEdit_address1.text()
        if not address1:
            invalidFlags.append('Address1')
        address2 = self.lineEdit_address2.text()

        province = self.lineEdit_province.text()
        if not province:
            invalidFlags.append('Province')

        country = self.lineEdit_country.text()
        if not country:
            invalidFlags.append('Country')

        zipcode = self.lineEdit_zipcode.text()
        if not zipcode:
            invalidFlags.append('Zipcode')

        phonenumber = self.lineEdit_phonenumber.text()
        if not phonenumber:
            invalidFlags.append('Phone Number')


        if len(invalidFlags) == 0:
            self.editProfile(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                      phonenumber)
        else:
            QtWidgets.QMessageBox.warning(self, "Cannot register", "Invalid information:\n"+str(invalidFlags))



    def editProfile(self, username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                 phonenumber):
        Users().updateUser(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                      phonenumber)
        QtWidgets.QMessageBox.information(self, "Notification", "Edit Profile complete!")
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editProfileDialog = EditProfileDialog(user_id=1, DEBUGMODE=True)
    editProfileDialog.show()
    sys.exit(app.exec_())