from PyQt5 import QtWidgets, QtCore


class EditTextWidget(QtWidgets.QTextEdit):

    def __init__(self, model, parent=None):
        super(EditTextWidget, self).__init__(parent)

        self.__model = model
        self.__setup_ui()

    def __setup_ui(self):
        self.setGeometry(0, 0, 400, 400)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)

    def wheelEvent(self, event):
        super(EditTextWidget, self).wheelEvent(event)

        self.__model.generate_template(self.toPlainText())
        self.__render_template()

        anchor = self.anchorAt(event.pos())
        if anchor:
            self.__change_value(anchor, event.angleDelta().y())

    def __change_value(self, val_id, amount):
        self.__model.set_number_position_value(val_id, amount)
        self.__render_template()

    def __render_template(self):
        cursor = self.textCursor()
        self.setHtml(self.__model.create_doc())
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self, event)
        self.__model.handle_key_event(event, self.toPlainText())
