from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtGui

class ClickableWidget(QWidget):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(QtGui.QCursor(Qt.ClosedHandCursor))
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(QtGui.QCursor(Qt.OpenHandCursor))
        super().mouseReleaseEvent(event)