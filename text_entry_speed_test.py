#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout

from config_parser import ConfigParser
from text_input_technique import EditTextWidget
from text_model import TextModel, KeyboardType

"""
The features of the program were discussed together and everyone got their own tasks.
"""


# Author: Claudia, Sarah
# Reviewer: Sarah
class MainWindow(QtWidgets.QWidget):

    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.__model = TextModel(config)

        self.setFixedSize(800, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())

        self.setWindowTitle("Typing Speed Test")

        example_text = QtWidgets.QLabel(self)
        example_text.setFont(QFont("Arial", 15))
        example_text.setText(self.__model.get_example_text().strip())
        example_text.setAlignment(QtCore.Qt.AlignLeft)
        self.__example_text = example_text

        self.__edit_text = EditTextWidget(self.__model, self)
        self.__setup_completer()

        layout = QVBoxLayout(self)
        layout.addWidget(self.__example_text)
        layout.addWidget(self.__edit_text)
        self.setLayout(layout)

        self.__model.test_finished.connect(self.__close_program)
        self.__show_hint()

    def __setup_completer(self):
        if self.__model.get_keyboard_type() == KeyboardType.AUTO_COMPLETE.value:
            completer = QtWidgets.QCompleter(
                self.__model.get_word_list(), self)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setWrapAround(False)
            self.__edit_text.set_completer(completer)

    def __show_hint(self):
        QtWidgets.QMessageBox.information(self,
                                          "Introduction",
                                          "Type the text as shown above,\nfinish every line with 'Enter'")

    def __close_program(self):
        if self.__model.get_clean_content():
            QtWidgets.QMessageBox.information(
                self, "Test passed", "Test finished")
        else:
            QtWidgets.QMessageBox.warning(self, "Test failed", "Lazy bastard")

        QtWidgets.qApp.quit()


def main():
    config_parser = ConfigParser()

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(config_parser.get_config())
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
