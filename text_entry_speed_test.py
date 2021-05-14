#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from config_parser import ConfigParser
from edit_text_widget import EditTextWidget
from text_model import TextModel

"""
The features of the program were discussed together and everyone got their own tasks.
The authors of the python and sub files are written at the beginning of the python files.
"""


class MainWindow(QtWidgets.QWidget):

    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.__model = TextModel(config)  # TODO all widgets share the same model

        self.setFixedSize(800, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(self).center() - self.rect().center())

        self.setWindowTitle("Typing Speed Test")

        self.__setup_typing_speed_display()
        self.__setup_example_text()

        self.edit_text = EditTextWidget(self.__model, self)

        layout = QVBoxLayout(self)  # or QGridLayout
        layout.addWidget(self.typing_speed_display)
        layout.addWidget(self.example_text)
        layout.addWidget(self.edit_text)
        self.setLayout(layout)

    def __setup_example_text(self):
        self.example_text = QLabel(self)
        self.example_text.setFont(QFont("Arial", 15))
        self.example_text.setText(self.__model.get_example_text())
        self.example_text.setAlignment(QtCore.Qt.AlignCenter)

    def __setup_typing_speed_display(self):
        # TODO should we display the time or is it sufficient to log the time
        # self.typing_speed_display = TypingSpeedDisplay(self) # this is not working
        self.typing_speed_display = QLabel(self)
        self.typing_speed_display.setFont(QFont("Arial", 15))
        self.typing_speed_display.setText("Speed")
        self.typing_speed_display.setAlignment(QtCore.Qt.AlignCenter)


def main():
    config_parser = ConfigParser()

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(config_parser.get_config())
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
