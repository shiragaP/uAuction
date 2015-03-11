

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