from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont


class ExampleTextDisplay(QtWidgets.QLabel):

    def __init__(self, model, parent=None):
        super(ExampleTextDisplay, self).__init__(parent)

        self.__model = model
        self.setFont(QFont("Arial", 15))
        self.setText(self.__model.get_example_text())
        self.setAlignment(QtCore.Qt.AlignCenter)
