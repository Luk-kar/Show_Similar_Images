import sys
import os
from tkinter import filedialog  # for Python 3
from configparser import ConfigParser
from datetime import datetime

from .paths import get_AppData_folder_path, get_DEFAULTS_folder_path


class Logger:
    def __init__(self):
        self.AppData_folder_path = get_AppData_folder_path()
        self.DEFAULTS_folder_path = get_DEFAULTS_folder_path(
            self.AppData_folder_path)

        self.file_path = os.path.join(
            self.DEFAULTS_folder_path,
            "LOGGER.ini"
        )

        self.sections = {
            "LOGGER": {
                "key": "save founded matches to log",
                "value": 1
            }
        }

    def create_DEFAULT_file(self):

        logger_path = self.file_path

        key = self.sections["LOGGER"]["key"]
        value = self.sections["LOGGER"]["value"]

        option = [key, value]

        self.saving_logger_to_file(
            logger_path,
            option
        )

    def set_writing_status(self, value):

        logger_path = self.file_path

        key = self.sections["LOGGER"]["key"]
        option = [key, value]

        self.saving_logger_to_file(
            logger_path,
            option
        )

    def saving_logger_to_file(
            self,
            logger_path,
            option
    ):

        config = ConfigParser()

        config["LOGGER"] = {
            option[0]: option[1],
        }

        if logger_path:
            with open(logger_path, "w") as configfile:
                config.write(configfile)
        else:
            raise OSError("There is no save path")

    def read_config_file(self, file):
        """return string"""

        config = ConfigParser()

        try:
            with open(file) as f:
                config.read_file(f)
        except IOError as error:
            raise IOError(error)

        return config

    def read_writing_status(self):

        AppData = self.AppData_folder_path
        DEFAULTS_folder = self.DEFAULTS_folder_path
        LOGGER = self.file_path

        if not os.path.isdir(AppData):
            os.mkdir(AppData)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        if not os.path.exists(LOGGER):
            self.create_DEFAULT_file()

        config = self.read_config_file(LOGGER)
        value = int(config.get("LOGGER", "save founded matches to log"))

        return value

    @staticmethod
    def create_log_of_similar_images(similar_images, similarity, dir_output):

        def get_current_date():
            """get the current date"""

            datetime_object = datetime.now()
            return datetime_object.strftime("%Y_%m_%d-%H_%M")

        to_write_down = f"{os.path.dirname(dir_output)}\nsimilarity: {similarity}\n"

        for image_list in similar_images:

            if len(similar_images[image_list]) > 1:

                to_write_down += "\n"

                for img in similar_images[image_list]:
                    to_write_down += f"{os.path.basename(img)}\n"

        current_date = get_current_date()
        file_path = os.path.join(dir_output, f"{current_date}-list.log")
        file_log = open(file_path, "w")
        file_log.writelines(to_write_down)
        file_log.close()
