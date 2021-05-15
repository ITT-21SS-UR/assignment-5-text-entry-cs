#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout

from config_parser import ConfigParser
from example_text_display import ExampleTextDisplay
from text_input_technique import EditTextWidget
from text_model import TextModel, KeyboardType

"""
The features of the program were discussed together and everyone got their own tasks.
"""


# Author: Claudia
# Reviewer: Sarah
class MainWindow(QtWidgets.QWidget):

    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.__model = TextModel(config)

        self.setFixedSize(800, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(self).center() - self.rect().center())

        self.setWindowTitle("Typing Speed Test")

        self.__example_text = ExampleTextDisplay(self.__model, self)
        self.__edit_text = EditTextWidget(self.__model, self)
        self.__setup_completer()

        layout = QVBoxLayout(self)
        layout.addWidget(self.__example_text)
        layout.addWidget(self.__edit_text)
        self.setLayout(layout)

        self.__model.test_finished.connect(self.__close_program)

    def __setup_completer(self):
        if self.__model.get_keyboard_type() == KeyboardType.AUTO_COMPLETE.value:
            completer = QtWidgets.QCompleter(self.__model.get_word_list(), self)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setWrapAround(False)
            self.__edit_text.set_completer(completer)

    @staticmethod
    def __close_program():
        sys.exit(0)


def main():
    config_parser = ConfigParser()

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(config_parser.get_config())
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
