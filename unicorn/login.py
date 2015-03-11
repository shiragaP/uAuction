
import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtUiTools

class LoginWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\login.ui')

        self.label_logo = form.findChild(QtGui.QLabel, 'label_00_logo')
        self.label_logo.setPixmap(QtGui.QPixmap('..\\resources\\img\\logo.png'))

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loginWidget = LoginWidget()
    loginWidget.show()
    sys.exit(app.exec_())