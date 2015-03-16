__author__ = 'Waterstrider'
from sys import argv

from PySide.QtCore import *
from PySide.QtGui import *

class UThumbnailDetailItem(QListWidgetItem):
    def __init__(self, filepath,  parent=None):
        QListWidgetItem.__init__(self, parent)

        try:
            filepath = str(filepath)
        except:
            return -1                                                   # TODO: add warning

        thumbnailWidth = thumbnailHeight = 75
        self.thumbnailImage = QImage(filepath)
        self.thumbnailLabel = QLabel("<Thumbnail>")
        self.thumbnailLabel.setStyleSheet("border: 1px solid grey")
        self.thumbnailLabel.setPixmap(QPixmap(self.thumbnailImage.scaled(thumbnailWidth, thumbnailHeight, Qt.KeepAspectRatio)))
        self.thumbnailLabel.setMinimumSize(thumbnailWidth, thumbnailHeight)
        self.thumbnailLabel.setMaximumSize(thumbnailWidth, thumbnailHeight)
        self.thumbnailLabel.setAlignment(Qt.AlignCenter)

        filename = filepath[max(filepath.rfind('\\'), filepath.rfind('/')) + 1:]
        width = self.thumbnailImage.width()
        height = self.thumbnailImage.height()
        depth = self.thumbnailImage.depth()
        detailsGridLayout = QGridLayout(None)
        detailsGridLayout.addWidget(QLabel("Filename: " + filename), 0, 0, 1, 1)
        detailsGridLayout.addWidget(QLabel("Width: " + str(width) + " px"), 1, 0, 1, 1)
        detailsGridLayout.addWidget(QLabel("Height: " + str(height) + " px"), 2, 0, 1, 1)
        detailsGridLayout.addWidget(QLabel("Bit Depth: " + str(depth)), 3, 0, 1, 1)

        self.thumbnailWidget = QWidget()
        self.gridLayout = QGridLayout(self.thumbnailWidget)
        self.gridLayout.addWidget(self.thumbnailLabel, 0, 0, 1, 1)
        self.gridLayout.addLayout(detailsGridLayout, 0, 1, 1, 1)
        self.thumbnailWidget.setLayout(self.gridLayout)

        self.setSizeHint(self.thumbnailWidget.sizeHint())