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
We helped each other while programming. The workload was distributed evenly.

HOW TO START THE PROGRAM:
python3 text_entry_speed_test.py config.json

Config file structure with description:
{
  "participant_id": 1,
  "keyboard_type": "normal",  # 2 possible values: normal, auto_complete
  "txt_file": "test.txt",  # for the study we used 2 different txt files, which were copied from books
  "key_limit": 2  # how many characters should be typed, so that auto-completion is invoked if enabled
}

"""


# Author: Claudia, Sarah
# Reviewer: Sarah
class MainWindow(QtWidgets.QWidget):

    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.__model = TextModel(config)

        self.setFixedSize(810, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())

        self.setWindowTitle("Tippgeschwindigkeitstest")

        self.__setup_example_text()
        self.__edit_text = EditTextWidget(self.__model, self)
        self.__setup_completer()

        self.__setup_layout()

        self.__model.test_finished.connect(self.__close_program)
        self.__show_hint()

    def __setup_example_text(self):
        example_text = QtWidgets.QLabel(self)
        example_text.setFont(QFont("Arial", 15))
        example_text.setText(self.__model.get_example_text().strip())
        example_text.setAlignment(QtCore.Qt.AlignLeft)
        self.__example_text = example_text

    def __setup_completer(self):
        if self.__model.get_keyboard_type() == KeyboardType.AUTO_COMPLETE.value:
            completer = QtWidgets.QCompleter(
                self.__model.get_word_list(), self)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setModelSorting(QtWidgets.QCompleter.CaseInsensitivelySortedModel)
            completer.setWrapAround(False)
            self.__edit_text.set_completer(completer)

    def __setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.__example_text)
        layout.addWidget(self.__edit_text)
        self.setLayout(layout)

    def __show_hint(self):
        QtWidgets.QMessageBox.information(self,
                                          "Einleitung",
                                          "Tippen Sie den Text wie oben abgebildet ein,\
                                              \n und schließen Sie jede Zeile mit 'Enter' ab \
                                              \n (inklusive der letzten).")

    def __close_program(self):
        if self.__model.get_clean_content():
            QtWidgets.QMessageBox.information(
                self, "Test bestanden", "Test erfolgreich beendet :)")
        else:
            QtWidgets.QMessageBox.warning(
                self, "Test gescheitert", "Fauler Hund!")

        QtWidgets.qApp.quit()


def main():
    config_parser = ConfigParser()

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(config_parser.get_config())
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
