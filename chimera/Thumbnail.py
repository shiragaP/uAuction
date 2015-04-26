__author__ = 'Waterstrider'

import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class ThumbnailWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, filepath, thumbnailWidth, thumbnailHeight, parent=None):
        super().__init__(parent)
        self.filepath = filepath
        self.thumbnailWidth = thumbnailWidth
        self.thumbnailHeight = thumbnailHeight

        self.thumbnailImage = QtGui.QImage(self.filepath)
        #self.thumbnailImage.loadFromData(self.filepath)
        self.thumbnailLabel = QtWidgets.QLabel("<Thumbnail>")
        self.thumbnailLabel.setStyleSheet("border: 1px solid grey")
        self.thumbnailLabel.setPixmap(QtGui.QPixmap(
            self.thumbnailImage.scaled(self.thumbnailWidth, self.thumbnailHeight, QtCore.Qt.KeepAspectRatio)))
        self.thumbnailLabel.setMinimumSize(self.thumbnailWidth, self.thumbnailHeight)
        self.thumbnailLabel.setMaximumSize(self.thumbnailWidth, self.thumbnailHeight)
        self.thumbnailLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thumbnailWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.thumbnailWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.thumbnailLabel, 0, 0, 1, 1)
        self.thumbnailWidget.setLayout(self.gridLayout)

        self.setSizeHint(self.thumbnailWidget.sizeHint())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    thumbnailWidgetItem = ThumbnailWidgetItem("C:\\Users\\Fujiwara\\Pictures\\Kantai Collection\\Hinagiku55.png",
                                              600, 600)
    thumbnailWidgetItem.thumbnailWidget.show()
    sys.exit(app.exec_())