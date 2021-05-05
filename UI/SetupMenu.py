import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config import set_app_path

from UI.helpers.open_folder import open_folder


def get_DEFAULT_ini_path():
    return os.path.join(set_app_path(), "appData")


def get_save_file_ini_path():
    return filedialog.asksaveasfilename(initialdir=get_DEFAULT_ini_path(), title="Save setup file", filetypes=[("Setup files", "*.ini")])


def get_open_file_ini_path():
    return filedialog.askopenfilename(initialdir=get_DEFAULT_ini_path(), title="Open setup file", filetypes=[("Setup files", "*.ini")])


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


def read_config_file(file):
    """return string"""

    config = ConfigParser()

    try:
        with open(file) as f:
            config.read_file(f)
    except IOError as error:
        raise IOError(error)

    return config


DEFAULTS_file_path = "_DEFAULT.ini"


def get_images_folder_path(config):
    return config.get("MATCHING", "images path")


def get_similarity(config):
    return config.get("MINIMAL SIMILARITY", "value")


def get_checked_extensions(config):
    return config.items("FILE TYPES")


def create_DEFAULT_setup_file(setup_path):
    valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
    checkedboxes = list(map(lambda x: x[1], valid_extensions))
    target_path = ""
    similarity = 0.8

    setup_saving_to_ini(
        setup_path,
        checkedboxes,
        target_path,
        similarity
    )


# https://stackoverflow.com/questions/31170616/how-to-access-a-method-in-one-inherited-tkinter-class-from-another-inherited-tki
class SetupMenu(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        self.main = main
        self.ini_default_location = get_DEFAULT_ini_path()

        setupMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Setup", underline=0, menu=setupMenu)
        setupMenu.add_command(
            label="Save as", command=self.setup_save_as)
        setupMenu.add_command(label="Open", command=self.setup_open)
        setupMenu.add_command(label="Save to defaults",
                              command=self.setup_save_to_defaults)
        setupMenu.add_command(label="Reset to defaults",
                              command=self.setup_reset_to_defaults)
        setupMenu.add_command(label="Defaults reset",
                              command=self.setup_default_reset)
        setupMenu.add_separator()
        setupMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)

    def setup_save_as(self):

        main = self.main

        setup_path = get_save_file_ini_path()

        if setup_path:
            checkedboxes = list(main.checkbars.state())
            target_path = main.target_path_entry.get()
            similarity = float(main.similarity_entry.get())

            setup_saving_to_ini(
                setup_path,
                checkedboxes,
                target_path,
                similarity
            )

            messagebox.showinfo(
                "Done!",
                "You saved setup file in:"f"\n{setup_path}"
            )

            setup_folder = os.path.dirname(setup_path)
            open_folder(setup_folder)

        else:

            messagebox.showinfo(
                "Ouch!",
                "You haven't saved config!"
            )

    def setup_open(self):

        setup_path = get_open_file_ini_path()

        if setup_path:
            config = read_config_file(setup_path)
            self.dialogs_set_setup(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def setup_save_to_defaults(self):

        main = self.main

        setup_path = os.path.join(
            self.ini_default_location, DEFAULTS_file_path)
        checkedboxes = list(main.checkbars.state())
        target_path = main.target_path_entry.get()
        similarity = float(main.similarity_entry.get())

        setup_saving_to_ini(
            setup_path,
            checkedboxes,
            target_path,
            similarity
        )

    def setup_reset_to_defaults(self):
        setup_path = os.path.join(
            self.ini_default_location, DEFAULTS_file_path)

        if not os.path.exists(setup_path):

            create_DEFAULT_setup_file(setup_path)

        config = read_config_file(setup_path)
        self.dialogs_set_setup(config)

    def setup_default_reset(self):
        setup_path = os.path.join(
            self.ini_default_location, DEFAULTS_file_path)

        create_DEFAULT_setup_file(setup_path)

        config = read_config_file(setup_path)
        self.dialogs_set_setup(config)

    def dialogs_set_setup(self, config):

        main = self.main

        main.target_path_entry = main.entry_set(
            main.target_path_entry, get_images_folder_path(config)
        )

        picks = get_checked_extensions(config)
        main.checkbars.set_state(picks)

        main.similarity_entry = main.entry_set(
            main.similarity_entry, get_similarity(config)
        )
