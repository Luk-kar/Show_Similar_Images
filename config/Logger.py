import sys
import os
from tkinter import filedialog  # for Python 3
from configparser import ConfigParser


class Logger:
    def __init__(self):
        self.AppData_folder_path = self.get_AppData_folder_path()
        self.DEFAULTS_folder_path = self.get_DEFAULTS_folder_path(
            self.AppData_folder_path)

        self.file_path = os.path.join(
            self.DEFAULTS_folder_path,
            "LOGGER.ini"
        )

    def get_AppData_folder_path(self):

        appData_folder = os.path.join(self.set_app_path(), "appData")
        if not os.path.isdir(appData_folder):
            os.mkdir(appData_folder)

        appData_folder = os.path.abspath(appData_folder)
        return appData_folder

    def get_DEFAULTS_folder_path(self, AppData_path):

        DEFAULTS_folder_path = os.path.join(
            AppData_path,
            "_DEFAULTS"
        )
        if not os.path.isdir(DEFAULTS_folder_path):
            os.mkdir(DEFAULTS_folder_path)

        return DEFAULTS_folder_path

    @staticmethod
    def set_app_path():

        # https://stackoverflow.com/a/404750/12490791
        program_name = sys.argv[0]

        if getattr(sys, 'frozen', False) or program_name.endswith("__main__.py"):
            application_path = ""  # relative ./
        elif __file__:
            application_path = f"{program_name}/"
        else:
            raise IOError("no path")

        return application_path

    def create_DEFAULT_file(self):

        logger_path = self.file_path

        option = ["save founded matches to log", 1]

        self.saving_dialogs_to_file(
            logger_path,
            option
        )

    @staticmethod
    def saving_dialogs_to_file(
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
