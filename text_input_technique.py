from PyQt5 import QtWidgets, QtCore, QtGui


# Sources:
# https://doc.qt.io/qt-5/qcompleter.html
# Main source for autocomplete, also the text for our comments are directly copied from the following source:
# https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html
# For python specific reference:
# https://www.howtobuildsoftware.com/index.php/how-do/IFK/python-3x-autocomplete-pyqt-qtextedit-pyqt5-pyqt5-qtextedit-auto-completion


# Author: Claudia
# Reviewer: Sarah
class EditTextWidget(QtWidgets.QTextEdit):

    def __init__(self, model, parent=None):
        super(EditTextWidget, self).__init__(parent)

        self.__model = model
        self.__setup_ui()
        self.__completer = None

    def __setup_ui(self):
        self.setGeometry(0, 0, 400, 400)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)

    def __change_value(self, val_id, amount):
        self.__model.set_number_position_value(val_id, amount)
        self.__render_template()

    def __render_template(self):
        cursor = self.textCursor()
        self.setHtml(self.__model.create_doc())
        self.setTextCursor(cursor)

    def __insert_completion(self, completion):
        # The __insert_completion() function is responsible for completing the word using a QTextCursor object, tc.
        if self.__completer.widget() != self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self.__completer.completionPrefix())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def __text_under_cursor(self):
        # The __text_under_cursor() function uses a QTextCursor, tc, to select a word under the cursor and return it.
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)

        return tc.selectedText()

    def focusInEvent(self, event):
        # The TextEdit class reimplements focusInEvent() function,
        # which is an event handler used to receive keyboard focus events for the widget.
        if self.__completer:
            self.__completer.setWidget(self)
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def wheelEvent(self, event):
        super(EditTextWidget, self).wheelEvent(event)

        self.__model.generate_template(self.toPlainText())
        self.__render_template()

        anchor = self.anchorAt(event.pos())
        if anchor:
            self.__change_value(anchor, event.angleDelta().y())

    def set_completer(self, completer):
        # The set_completer() function accepts a completer and sets it up.
        if self.__completer:
            self.disconnect(self)

        self.__completer = completer

        if not self.__completer:
            return

        self.__completer.setWidget(self)
        self.__completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.__completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.__completer.activated.connect(self.__insert_completion)

    def keyPressEvent(self, event):
        key_code = event.key()
        key_text = event.text()

        self.__model.handle_key_event(event, self.toPlainText())

        # The keyPressEvent() is reimplemented to ignore key events like
        # Qt::Key_Enter, Qt::Key_Return, Qt::Key_Escape, Qt::Key_Tab,
        # and Qt::Key_Backtab so the completer can handle them.
        # If there is an active completer, we cannot process the shortcut, Ctrl+E.
        if self.__completer \
                and self.__completer.popup().isVisible():

            if key_code in (
                    QtCore.Qt.Key_Enter,
                    QtCore.Qt.Key_Return,
                    QtCore.Qt.Key_Escape,
                    QtCore.Qt.Key_Tab,
                    QtCore.Qt.Key_Backtab):
                event.ignore()
                return  # let the completer do default behavior

        is_shortcut = (event.modifiers() == QtCore.Qt.ControlModifier
                       and key_code == QtCore.Qt.Key_E)  # CTRL+E

        if not self.__completer or not is_shortcut:  # do not process the shortcut when we have a completer
            QtWidgets.QTextEdit.keyPressEvent(self, event)

        # We also handle other modifiers and shortcuts for which we do not want the completer to respond to.
        ctrl_or_shift = (event.modifiers() == QtCore.Qt.ControlModifier
                         or event.modifiers() == QtCore.Qt.ShiftModifier)

        if not self.__completer \
                or (ctrl_or_shift and not key_text):
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # end of word
        has_modifier = ((event.modifiers() != QtCore.Qt.NoModifier)
                        and not ctrl_or_shift)

        completion_prefix = self.__text_under_cursor()

        if (not is_shortcut
                and (has_modifier
                     or not key_text
                     or len(completion_prefix) < 3
                     or key_text[-1] in eow)):
            self.__completer.popup().hide()
            return

        if completion_prefix != self.__completer.completionPrefix():  # TODO this is not working correctly
            self.__completer.setCompletionPrefix(completion_prefix)
            self.__completer.popup().setCurrentIndex(self.__completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.__completer.popup().sizeHintForColumn(0)
                    + self.__completer.popup().verticalScrollBar().sizeHint().width())
        self.__completer.complete(cr)  # popup it up!
