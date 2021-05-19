from PyQt5 import QtWidgets, QtCore, QtGui

from text_model import KeyboardType

"""
Our method for a faster text input is auto-completion.
When a user types a certain number of characters (set in config.json as key_limit),
auto-completion will display a list of suggested words.
With the arrow keys and confirming the selection with Enter, a suggestion can be selected.
Furthermore a user can manually invoke auto-completion by pressing Ctrl plus Space to select a word.

Sources:
https://doc.qt.io/qt-5/qcompleter.html

Main source for auto-complete (adjusted to our needs),
also the text for our comments are directly copied from the following source:
https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html

For python specific reference:
https://www.howtobuildsoftware.com/index.php/how-do/IFK/python-3x-autocomplete-pyqt-qtextedit-pyqt5-pyqt5-qtextedit-auto-completion
"""


# Author: Claudia, Sarah
# Reviewer: Sarah
class EditTextWidget(QtWidgets.QTextEdit):

    def __init__(self, model, parent=None):
        super(EditTextWidget, self).__init__(parent)

        self.__model = model
        self.__completer = None
        self.__key_limit = self.__model.get_key_limit()
        self.__setup_ui()

    def __setup_ui(self):
        self.setGeometry(0, 0, 400, 400)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

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

    def __handle_normal_keyboard(self, event):
        if (self.__model.is_ctrl_or_shift_or_caps_lock(event)
                and not event.text()):
            return

        super(EditTextWidget, self).keyPressEvent(event)
        self.__model.handle_key_event(event, self.toPlainText())

    def __handle_auto_complete(self, event):
        key_code = event.key()
        key_text = event.text()

        # The keyPressEvent() is reimplemented to ignore key events like
        # Qt::Key_Enter, Qt::Key_Return, Qt::Key_Escape, Qt::Key_Tab,
        # and Qt::Key_Backtab so the completer can handle them.
        # If there is an active completer, we cannot process the shortcut, Ctrl+Space.
        if (self.__completer
                and self.__completer.popup().isVisible()):

            if key_code in (
                    QtCore.Qt.Key_Enter,
                    QtCore.Qt.Key_Return,
                    QtCore.Qt.Key_Escape,
                    QtCore.Qt.Key_Tab,
                    QtCore.Qt.Key_Backtab):
                event.ignore()
                return  # let the completer do default behavior

        is_shortcut = (event.modifiers() == QtCore.Qt.ControlModifier
                       and key_code == QtCore.Qt.Key_Space)  # Ctrl+Space

        if (not self.__completer
                or not is_shortcut):  # do not process the shortcut when we have a completer
            super(EditTextWidget, self).keyPressEvent(event)

        # We also handle other modifiers and shortcuts for which we do not want the completer to respond to.
        ctrl_or_shift = self.__model.is_ctrl_or_shift_or_caps_lock(event)

        if (not self.__completer
                or (ctrl_or_shift and not key_text)):
            return

        self.__model.handle_key_event(event, self.toPlainText())

        has_modifier = ((event.modifiers() != QtCore.Qt.NoModifier)
                        and not ctrl_or_shift)

        completion_prefix = self.__text_under_cursor()
        self.__completer.setCompletionPrefix(completion_prefix)

        if (not is_shortcut
                and (has_modifier
                     or not key_text
                     or len(completion_prefix) < self.__key_limit
                     or self.__model.is_word_end(key_text[-1]))):
            self.__completer.popup().hide()
            return

        if (self.__completer.completionCount() == 1
                and self.__completer.currentCompletion().lower() == completion_prefix.lower()):
            return self.__completer.popup().hide()

        self.__completer.popup().setCurrentIndex(
            self.__completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.__completer.popup().sizeHintForColumn(0)
                    + self.__completer.popup().verticalScrollBar().sizeHint().width())
        self.__completer.complete(cr)  # popup it up!

    def focusInEvent(self, event):
        # The TextEdit class reimplements focusInEvent() function,
        # which is an event handler used to receive keyboard focus events for the widget.
        if self.__completer:
            self.__completer.setWidget(self)

        super(EditTextWidget, self).focusInEvent(event)

    def set_completer(self, completer):
        # The set_completer() function accepts a completer and sets it up.
        if self.__completer:
            self.disconnect(self)

        self.__completer = completer

        if not self.__completer:
            return

        self.__completer.setWidget(self)
        self.__completer.setCompletionMode(
            QtWidgets.QCompleter.PopupCompletion)
        self.__completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.__completer.activated.connect(self.__insert_completion)

    def keyPressEvent(self, event):
        if self.__model.get_keyboard_type() == KeyboardType.AUTO_COMPLETE.value:
            self.__handle_auto_complete(event)

        else:  # normal keyboard type
            self.__handle_normal_keyboard(event)
