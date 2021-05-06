import sys
import os
from tkinter import filedialog  # for Python 3
from configparser import ConfigParser


class Dialogs:
    def __init__(self):
        self.AppData_folder_path = self.get_AppData_folder_path()
        self.DEFAULTS_folder_path = self.get_DEFAULTS_folder_path(
            self.AppData_folder_path)

        self.DEFAULT_file_path = os.path.join(
            self.DEFAULTS_folder_path,
            "DIALOGS.ini"
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

    def get_dialogs_path_save(self):
        return filedialog.asksaveasfilename(initialdir=self.AppData_folder_path, title="Save setup file", filetypes=[("Setup files", "*.ini")])

    def get_dialogs_path_open(self):
        return filedialog.askopenfilename(initialdir=self.AppData_folder_path, title="Open setup file", filetypes=[("Setup files", "*.ini")])

    @staticmethod
    def saving_dialogs_to_file(
            DIALOGS_path,
            checkedboxes,
            target_path,
            similarity
    ):

        config = ConfigParser()

        config["MATCHING"] = {
            "images path": target_path,
        }

        config["FILE TYPES"] = {
            ".png": checkedboxes[0],
            ".jpg/.jpeg": checkedboxes[1],
            ".bmp": checkedboxes[2]
        }

        config["MINIMAL SIMILARITY"] = {
            "value": similarity,
        }

        if DIALOGS_path:
            with open(DIALOGS_path, "w") as configfile:
                config.write(configfile)
        else:
            raise OSError("There is no save path")

    @staticmethod
    def read_config_file(file):
        """return string"""

        config = ConfigParser()

        try:
            with open(file) as f:
                config.read_file(f)
        except IOError as error:
            raise IOError(error)

        return config

    def read_DEFAULT(self):

        DEFAULT = self.DEFAULT_file_path
        if not os.path.exists(DEFAULT):
            self.create_DEFAULT_file()

        config = self.read_config_file(DEFAULT)
        return config

    @staticmethod
    def get_images_folder_path(config):
        return config.get("MATCHING", "images path")

    @staticmethod
    def get_similarity(config):
        return config.get("MINIMAL SIMILARITY", "value")

    @staticmethod
    def get_checked_extensions(config):
        return config.items("FILE TYPES")

    def create_DEFAULT_file(self):

        DIALOGS_path = self.DEFAULT_file_path

        valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
        checkedboxes = list(map(lambda x: x[1], valid_extensions))
        target_path = ""
        similarity = 0.8

        self.saving_dialogs_to_file(
            DIALOGS_path,
            checkedboxes,
            target_path,
            similarity
        )

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
