from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class TypingSpeedDisplay(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TypingSpeedDisplay, self).__init__()

        self.speed_label = QLabel(parent)
        self.speed_label.setFont(QFont("Arial", 15))
        self.speed_label.setText("Speed")
        # self.speed_label.setAlignment(QtCore.Qt.AlignCenter)
