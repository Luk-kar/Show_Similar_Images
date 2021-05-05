import sys
import os
from tkinter import filedialog  # for Python 3
from configparser import ConfigParser

valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
similarity = 0.8


class Config:
    def __init__(self):
        self.DEFAULT_ini_path = os.path.abspath(self.get_DEFAULT_ini_path())
        self.DEFAULTS_file_path = os.path.abspath(os.path.join(
            self.DEFAULT_ini_path,
            "_DEFAULT.ini"
        ))

    def get_DEFAULT_ini_path(self):
        return os.path.join(self.set_app_path(), "appData")

    def get_save_file_ini_path(self):
        return filedialog.asksaveasfilename(initialdir=self.DEFAULT_ini_path, title="Save setup file", filetypes=[("Setup files", "*.ini")])

    def get_open_file_ini_path(self):
        return filedialog.askopenfilename(initialdir=self.DEFAULT_ini_path, title="Open setup file", filetypes=[("Setup files", "*.ini")])

    @staticmethod
    def setup_saving_to_ini(
            setup_path,
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

        if setup_path:
            with open(setup_path, "w") as configfile:
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

    @staticmethod
    def get_images_folder_path(config):
        return config.get("MATCHING", "images path")

    @staticmethod
    def get_similarity(config):
        return config.get("MINIMAL SIMILARITY", "value")

    @staticmethod
    def get_checked_extensions(config):
        return config.items("FILE TYPES")

    def create_DEFAULT_setup_file(self):

        setup_path = self.DEFAULTS_file_path

        valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
        checkedboxes = list(map(lambda x: x[1], valid_extensions))
        target_path = ""
        similarity = 0.8

        self.setup_saving_to_ini(
            setup_path,
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
