import sys
import os
from tkinter import filedialog  # for Python 3
from configparser import ConfigParser

from .paths import get_AppData_folder_path, get_DEFAULTS_folder_path


class Dialogs:
    def __init__(self):
        self.AppData_folder_path = get_AppData_folder_path()
        self.DEFAULTS_folder_path = get_DEFAULTS_folder_path(
            self.AppData_folder_path)

        self.DEFAULT_file_path = os.path.join(
            self.DEFAULTS_folder_path,
            "DIALOGS.ini"
        )

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

    def get_DEFAULT(self):

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
