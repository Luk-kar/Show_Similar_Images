import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config import set_app_path

from UI.helpers.open_folder import open_folder


# https://stackoverflow.com/questions/31170616/how-to-access-a-method-in-one-inherited-tkinter-class-from-another-inherited-tki
class MenuBar(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        self.main = main
        self.ini_default_location = os.path.join(set_app_path(), "appData")

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

        setup_path = filedialog.asksaveasfilename(
            initialdir=self.ini_default_location,
            title="Save setup file",
            filetypes=[("Setup files", "*.ini")]
        )

        if setup_path:
            checkedboxes = list(main.checkbars.state())
            target_path = main.target_path_entry.get()
            similarity = float(main.similarity_entry.get())

            self.setup_saving(
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

        setup_file = filedialog.askopenfilename(
            initialdir=self.ini_default_location,
            title="Open setup file",
            filetypes=[("Setup files", "*.ini")]
        )

        if setup_file:
            config = self.read_config_file(setup_file)
            self.dialogs_set_setup(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def setup_save_to_defaults(self):

        main = self.main

        setup_path = os.path.join(self.ini_default_location, "_DEFAULT.ini")
        checkedboxes = list(main.checkbars.state())
        target_path = main.target_path_entry.get()
        similarity = float(main.similarity_entry.get())

        self.setup_saving(
            setup_path,
            checkedboxes,
            target_path,
            similarity
        )

    def setup_reset_to_defaults(self):
        setup_file = os.path.join(self.ini_default_location, "_DEFAULT.ini")

        if not os.path.exists(setup_file):

            valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
            checkedboxes = list(map(lambda x: x[1], valid_extensions))
            target_path = ""
            similarity = 0.8

            self.setup_saving(
                setup_file,
                checkedboxes,
                target_path,
                similarity
            )

        config = self.read_config_file(setup_file)
        self.dialogs_set_setup(config)

    def setup_default_reset(self):
        setup_file = os.path.join(self.ini_default_location, "_DEFAULT.ini")

        valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
        # https://stackoverflow.com/a/6800507/12490791
        checkedboxes = list(map(lambda x: x[1], valid_extensions))
        target_path = ""
        similarity = 0.8

        self.setup_saving(
            setup_file,
            checkedboxes,
            target_path,
            similarity
        )

        config = self.read_config_file(setup_file)
        self.dialogs_set_setup(config)

    def dialogs_set_setup(self, config):

        main = self.main

        main.target_path_entry = main.entry_set(
            main.target_path_entry, config.get("MATCHING", "images path")
        )

        picks = config.items("FILE TYPES")
        main.checkbars.set_state(picks)

        main.similarity_entry = main.entry_set(
            main.similarity_entry, config.get("MINIMAL SIMILARITY", "value")
        )

    def read_config_file(self, file):
        """return string"""

        config = ConfigParser()

        try:
            with open(file) as f:
                config.read_file(f)
        except IOError as error:
            raise IOError(error)

        return config

    def setup_saving(
            self,
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
