

## To waterslider

# create widget ui from ui/register.ui
# link every lineEdit to string
# when button pressed validate for each string according to example and explaination
# have bool to store for validation

__author__ = 'Shiraga-P'

import sys

from PySide import QtGui
from PySide import QtUiTools

class RegisterWidget(QtGui.QWidget):

    def __init__(self, parent=None, DEBUGMODE=False):
        super().__init__(parent)
        self.DEBUGMODE = DEBUGMODE

        loader = QtUiTools.QUiLoader(self)
        form = loader.load('ui\\register.ui')

        layout = QtGui.QGridLayout()
        layout.addWidget(form)

        self.setLayout(layout)

        self.setFixedWidth(form.width() + 15)
        self.setFixedHeight(form.height() + 15)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    registerWidget = RegisterWidget(DEBUGMODE=True)
    registerWidget.show()
    sys.exit(app.exec_())