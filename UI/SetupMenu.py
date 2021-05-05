import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config import Config
from UI.helpers.open_folder import open_folder


# https://stackoverflow.com/questions/31170616/how-to-access-a-method-in-one-inherited-tkinter-class-from-another-inherited-tki
class SetupMenu(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        self.main = main
        self.setup = Config()

        setupMenu = tk.Menu(parent, tearoff=False)
        parent.add_cascade(label="Setup", underline=0, menu=setupMenu)
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

        setup_path = self.setup.get_save_file_ini_path()

        if setup_path:
            checkedboxes = list(main.checkbars.state())
            target_path = main.target_path_entry.get()
            similarity = float(main.similarity_entry.get())

            self.setup.setup_saving_to_ini(
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

        else:

            messagebox.showinfo(
                "Ouch!",
                "You haven't saved config!"
            )

    def setup_open(self):

        setup_path = self.setup.get_open_file_ini_path()

        if setup_path:
            config = self.setup.read_config_file(setup_path)
            self.dialogs_set_setup(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def setup_save_to_defaults(self):

        main = self.main

        setup_path = self.setup.DEFAULTS_file_path

        checkedboxes = list(main.checkbars.state())
        target_path = main.target_path_entry.get()
        similarity = float(main.similarity_entry.get())

        self.setup.setup_saving_to_ini(
            setup_path,
            checkedboxes,
            target_path,
            similarity
        )

    def setup_reset_to_defaults(self):
        setup_path = self.setup.DEFAULTS_file_path

        if not os.path.exists(setup_path):

            self.setup.create_DEFAULT_setup_file()

        config = self.setup.read_config_file(setup_path)
        self.dialogs_set_setup(config)

    def setup_default_reset(self):
        setup_path = self.setup.DEFAULTS_file_path

        self.setup.create_DEFAULT_setup_file()

        config = self.setup.read_config_file(setup_path)
        self.dialogs_set_setup(config)

    def dialogs_set_setup(self, config):

        main = self.main

        main.target_path_entry = main.entry_set(
            main.target_path_entry, self.setup.get_images_folder_path(config)
        )

        picks = self.setup.get_checked_extensions(config)
        main.checkbars.set_state(picks)

        main.similarity_entry = main.entry_set(
            main.similarity_entry, self.setup.get_similarity(config)
        )
