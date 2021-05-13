#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets

from text_model import TextModel


class SuperText(QtWidgets.QTextEdit):

    def __init__(self, example_text):
        super(SuperText, self).__init__()

        self.setHtml(example_text)

        self.__model = TextModel()
        self.__model.generate_template(self.toPlainText())
        self.__render_template()
        self.__init_UI()

    def __init_UI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle("SuperText")
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)

    def wheelEvent(self, event):
        super(SuperText, self).wheelEvent(event)

        self.__model.generate_template(self.toPlainText())
        self.__render_template()

        anchor = self.anchorAt(event.pos())
        if anchor:
            self.__change_value(anchor, event.angleDelta().y())

    def __change_value(self, val_id, amount):
        self.__model.set_number_position_value(val_id, amount)
        self.__render_template()

    def __render_template(self):
        self.setHtml(self.__model.create_doc())

        cursor = self.textCursor()
        self.setTextCursor(cursor)


def main():
    app = QtWidgets.QApplication(sys.argv)

    super_text = SuperText("An 123 Tagen kamen 1342 Personen.")
    super_text.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
