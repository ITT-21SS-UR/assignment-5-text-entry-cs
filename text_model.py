import re
import sys
from datetime import datetime
from enum import Enum

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


# Author: Claudia
# Reviewer: Sarah
class ConfigKeys(Enum):
    PARTICIPANT_ID = "participant_id"
    KEYBOARD_TYPE = "keyboard_type"
    EXAMPLE_TEXT = "example_text"

    @staticmethod
    def get_all_values():
        return list(map(lambda v: v.value, ConfigKeys))


class KeyboardType(Enum):
    NORMAL = "normal"
    AUTO_COMPLETE = "auto_complete"
    # further keyboard types can be extended


class LogType(Enum):
    KEY_PRESSED = "key_pressed"
    WORD_TYPED = "word_finished"
    SENTENCE_TYPED = "sentence_finished"
    TEST_FINISHED = "test_finished"


class TextModel(QObject):
    LOG_TYPE = "log_type"
    KEY_CODE = "key_code"
    KEY_VALUE = "key_value"
    CONTENT = "content"

    TIMESTAMP = "timestamp"
    WORD_TIME = "word_time_in_s"
    SENTENCE_TIME = "sentence_time_in_s"
    WORDS_PER_MINUTE = "words_per_minute"

    INVALID_TIME = "NaN"

    test_finished = pyqtSignal()

    @staticmethod
    def __is_sentence_end(value):
        if value == QtCore.Qt.Key_Enter \
                or value == QtCore.Qt.Key_Return \
                or value == "\n":
            return True

        return False

    @staticmethod
    def __is_word_end(key_code):  # "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # TODO also for own word end
        if key_code == QtCore.Qt.Key_Space \
                or key_code == QtCore.Qt.Key_Colon \
                or key_code == QtCore.Qt.Key_Comma \
                or key_code == QtCore.Qt.Key_Semicolon \
                or key_code == QtCore.Qt.Key_Tab:
            # or key_code == QtCore.Qt.Key_Question \
            # or key_code == QtCore.Qt.Key_Exclam \
            # or key_code == QtCore.Qt.Key_Period:
            return True

        return False

    @staticmethod
    def __write_to_stdout_in_csv_format(row_data):
        row_data_values = list(row_data.values())
        values_length = len(row_data_values)

        for i in range(values_length):
            value = str(row_data_values[i])

            if i == values_length - 1:
                sys.stdout.write(value)
            else:
                sys.stdout.write(value + ";")

        sys.stdout.write("\n")
        sys.stdout.flush()

    def __init__(self, config):
        super().__init__()

        self.__config = config

        self.__numbers = []
        self.__template_doc = ""

        self.__content = ""

        self.__first_start_time = self.INVALID_TIME
        self.__word_start_time = self.INVALID_TIME
        self.__sentence_start_time = self.INVALID_TIME

        self.__sentence_count = 0
        self.__total_sentences = self.__calculate_number_sentences(self.get_example_text())

        self.__stdout_csv_column_names()

    def __calculate_number_sentences(self, text):
        sentence_number = 0

        for char in text:
            if self.__is_sentence_end(char):
                sentence_number += 1

        return sentence_number

    def __calculate_time_difference(self, start_time):
        end_time = datetime.now()

        try:
            return (end_time - start_time).total_seconds()
        except AttributeError:
            return self.INVALID_TIME
        except TypeError:
            return self.INVALID_TIME

    def __get_csv_columns(self):
        return [
            self.LOG_TYPE,
            ConfigKeys.PARTICIPANT_ID.value,
            ConfigKeys.KEYBOARD_TYPE.value,
            self.KEY_CODE,
            self.KEY_VALUE,
            self.CONTENT,
            self.TIMESTAMP,
            self.WORD_TIME,
            self.SENTENCE_TIME,
            self.WORDS_PER_MINUTE
        ]

    def __stdout_csv_column_names(self):
        for column_name in self.__get_csv_columns():
            if column_name == self.__get_csv_columns()[-1]:
                sys.stdout.write(str(column_name))
            else:
                sys.stdout.write(str(column_name) + ";")

        sys.stdout.write("\n")
        sys.stdout.flush()

    def __calculate_words_per_minute(self):
        minutes_since_typing_start = self.__calculate_time_difference(self.__first_start_time) / 60

        # characters per minute / 5
        return len(self.__content) / minutes_since_typing_start / 5

    def __create_row_data(self, key_event, log_type, word_time="NaN", sentence_time="NaN"):
        return {
            self.LOG_TYPE: log_type.value,
            ConfigKeys.PARTICIPANT_ID.value: self.get_participant_id(),
            ConfigKeys.KEYBOARD_TYPE: self.get_keyboard_type(),
            self.KEY_CODE: key_event.key(),
            self.KEY_VALUE: key_event.text(),
            self.CONTENT: self.__content,
            self.TIMESTAMP: datetime.now(),
            self.WORD_TIME: word_time,
            self.SENTENCE_TIME: sentence_time,
            self.WORDS_PER_MINUTE: self.__calculate_words_per_minute()
        }

    def __handle_sentence_end(self, key_event):
        self.__sentence_count = self.__calculate_number_sentences(self.__content)

        # TODO is not working correctly when enter/return is pressed
        word_time = self.__calculate_time_difference(self.__word_start_time)
        sentence_time = self.__calculate_time_difference(self.__sentence_start_time)

        if self.__sentence_count > self.__total_sentences:
            self.__write_to_stdout_in_csv_format(
                self.__create_row_data(key_event, LogType.TEST_FINISHED, word_time=word_time,
                                       sentence_time=sentence_time))
            self.test_finished.emit()

        else:
            self.__write_to_stdout_in_csv_format(
                self.__create_row_data(key_event, LogType.SENTENCE_TYPED, word_time=word_time,
                                       sentence_time=sentence_time))

        self.__word_start_time = self.INVALID_TIME
        self.__sentence_start_time = self.INVALID_TIME

    def __handle_word_end(self, key_event):
        word_time = self.__calculate_time_difference(self.__word_start_time)

        self.__write_to_stdout_in_csv_format(
            self.__create_row_data(key_event, LogType.WORD_TYPED, word_time=word_time))

        self.__word_start_time = self.INVALID_TIME

    def __handle_rest(self, key_event):
        if self.__word_start_time == self.INVALID_TIME:
            self.__word_start_time = datetime.now()

        if self.__sentence_start_time == self.INVALID_TIME:
            self.__sentence_start_time = datetime.now()

        self.__write_to_stdout_in_csv_format(self.__create_row_data(key_event, LogType.KEY_PRESSED))

    def __generate_word_list(self):
        return self.get_example_text().replace(" ", "\n").split("\n")

    def get_participant_id(self):
        return self.__config[ConfigKeys.PARTICIPANT_ID.value]

    def get_keyboard_type(self):
        return self.__config[ConfigKeys.KEYBOARD_TYPE.value]

    def get_example_text(self):
        return self.__config[ConfigKeys.EXAMPLE_TEXT.value]

    def get_word_list(self):
        return self.__generate_word_list()

    def set_number_position_value(self, val_id, amount):
        self.__numbers[int(str(val_id))] += amount / 120

    def create_doc(self):
        doc = self.__template_doc

        for num_id, num in enumerate(self.__numbers):
            doc = doc.replace("$" + str(num_id) + "$", "%d" % (num))

        return doc

    def generate_template(self, plaint_text):
        content = str(plaint_text)
        numbers = list(re.finditer(" -?[0-9]+", content))
        numbers = [int(n.group()) for n in numbers]

        self.__numbers = numbers

        if len(numbers) == 0:
            self.__template_doc = content
            return

        for num_id in range(len(numbers)):
            content = re.sub(" " + str(numbers[num_id]), " <a href='%d'>$%d$</a>" % (num_id, num_id), content, count=1)

        self.__template_doc = content

    def handle_key_event(self, key_event, text):
        self.__content = text

        if self.__first_start_time == self.INVALID_TIME:
            self.__first_start_time = datetime.now()

        key_code = key_event.key()
        if self.__is_sentence_end(key_code):
            self.__handle_sentence_end(key_event)
        elif self.__is_word_end(key_code):
            self.__handle_word_end(key_event)
        else:
            self.__handle_rest(key_event)
