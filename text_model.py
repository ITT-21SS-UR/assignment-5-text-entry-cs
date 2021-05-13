import re
import sys
from enum import Enum

from PyQt5.QtCore import QObject


class ConfigKeys(Enum):
    PARTICIPANT_ID = "participant_id"
    KEYBOARD_TYPE = "keyboard_type"


class LogType(Enum):
    KEY_PRESSED = "key_pressed"
    WORD_TYPED = "word_typed"
    SENTENCE_TYPED = "sentence_typed"
    TEST_FINISHED = "test_finished"


class TextModel(QObject):
    TIMESTAMP = "timestamp"

    def __init__(self):
        super().__init__()

        self.__numbers = []
        self.__template_doc = ""
        self.__prev_content = ""

        self.__stdout_csv_column_names()

    def __get_csv_columns(self):
        return [
            ConfigKeys.PARTICIPANT_ID.value,
            ConfigKeys.KEYBOARD_TYPE.value,
            self.TIMESTAMP
        ]

    def __stdout_csv_column_names(self):
        for column_name in self.__get_csv_columns():
            if column_name == self.__get_csv_columns()[-1]:
                sys.stdout.write(str(column_name))
            else:
                sys.stdout.write(str(column_name) + ",")

        sys.stdout.write("\n")
        sys.stdout.flush()

    def get_numbers(self):
        return self.__numbers

    def set_numbers(self, numbers):
        self.__numbers = numbers

    def set_number_position_value(self, val_id, amount):
        self.__numbers[int(str(val_id))] += amount / 120

    def get_template_doc(self):
        return self.__template_doc

    def set_template_doc(self, template_doc):
        self.__template_doc = template_doc

    def get_prev_content(self):
        return self.__prev_content

    def set_prev_content(self, prev_content):
        self.__prev_content = prev_content

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
