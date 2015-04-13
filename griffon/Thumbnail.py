__author__ = 'Waterstrider'

import sys

from PySide import QtCore
from PySide import QtGui


class ThumbnailWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, filepath, thumbnailWidth, thumbnailHeight, parent=None):
        self.filepath = filepath
        self.thumbnailWidth = thumbnailWidth
        self.thumbnailHeight = thumbnailHeight
        super().__init__(parent)

        try:
            filepath = str(filepath)
        except:
            return -1  # TODO: add warning

        self.thumbnailImage = QtGui.QImage()
        self.filepath.seek(0)
        self.thumbnailImage.loadFromData(self.filepath.read())
        self.thumbnailLabel = QtGui.QLabel("<Thumbnail>")
        self.thumbnailLabel.setStyleSheet("border: 1px solid grey")
        self.thumbnailLabel.setPixmap(QtGui.QPixmap(
            self.thumbnailImage.scaled(self.thumbnailWidth, self.thumbnailHeight, QtCore.Qt.KeepAspectRatio)))
        self.thumbnailLabel.setMinimumSize(self.thumbnailWidth, self.thumbnailHeight)
        self.thumbnailLabel.setMaximumSize(self.thumbnailWidth, self.thumbnailHeight)
        self.thumbnailLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thumbnailWidget = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout(self.thumbnailWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.thumbnailLabel, 0, 0, 1, 1)
        self.thumbnailWidget.setLayout(self.gridLayout)

        self.setSizeHint(self.thumbnailWidget.sizeHint())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    thumbnailWidgetItem = ThumbnailWidgetItem("E:\\Programming\\Pycharm Projects\\uAuction\\resources\\img\\logo.png",
                                              60, 60)
    thumbnailWidgetItem.thumbnailWidget.show()
    sys.exit(app.exec_())