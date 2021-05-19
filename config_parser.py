import json
import os
import sys

from text_model import ConfigKeys

"""
Responsilbe for parsing the json file for the config.
If the given config is invalid the system exists and prints out error messages.
"""


# Author: Claudia
class ConfigParser:
    @staticmethod
    def __exit_program(message="Please give a valid .json file as argument (-_-)\n"):
        sys.stderr.write(message)
        sys.exit(1)

    def __init__(self):
        self.__config = self.__read_test_config()
        self.__exit_if_not_valid_config()

    def __create_json_config(self):
        with open(self.file_name) as file:
            return json.load(file)

    def __read_test_config(self):
        if len(sys.argv) < 2:
            self.__exit_program()

        self.file_name = sys.argv[1]

        if not os.path.isfile(self.file_name):
            self.__exit_program("File does not exist (-_-)\n")

        file_extension = os.path.splitext(self.file_name)

        if file_extension[-1] == ".json":
            return self.__create_json_config()

        else:
            self.__exit_program()

    def __exit_if_not_valid_config(self):
        missing_key = False

        for key in ConfigKeys.get_all_values():

            if key not in self.__config:
                missing_key = True
                print("config: no {0} found".format(key))

        if missing_key:
            self.__exit_program()

    def get_config(self):
        return self.__config
