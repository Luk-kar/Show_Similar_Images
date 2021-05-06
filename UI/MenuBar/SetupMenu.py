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
            label="Save as", command=self.save_as_DIALOGS)
        setupMenu.add_command(label="Open", command=self.open_DIALOGS)
        setupMenu.add_command(label="Save to defaults",
                              command=self.save_to_default_DIALOGS)
        setupMenu.add_command(label="Reset to defaults",
                              command=self.reset_to_default_DIALOGS)
        setupMenu.add_command(label="Defaults reset",
                              command=self.reset_default_DIALOGS)
        setupMenu.add_separator()
        setupMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)

    def save_as_DIALOGS(self):

        main = self.main

        DIALOGS_path = self.setup.get_save_dialogs_to_file_path()

        if DIALOGS_path:
            checkedboxes = list(main.checkbars.state())
            target_path = main.target_path_entry.get()
            similarity = float(main.similarity_entry.get())

            self.setup.saving_dialogs_to_file(
                DIALOGS_path,
                checkedboxes,
                target_path,
                similarity
            )

            messagebox.showinfo(
                "Done!",
                "You saved setup file in:"f"\n{DIALOGS_path}"
            )

            setup_folder = os.path.dirname(DIALOGS_path)

        else:

            messagebox.showinfo(
                "Ouch!",
                "You haven't saved config!"
            )

    def open_DIALOGS(self):

        setup_path = self.setup.get_open_dialogs_file_path()

        if setup_path:
            config = self.setup.read_config_file(setup_path)
            self.dialogs_set_setup(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def save_to_default_DIALOGS(self):

        main = self.main

        setup_path = self.setup.DEFAULTS_DIALOGS_path

        checkedboxes = list(main.checkbars.state())
        target_path = main.target_path_entry.get()
        similarity = float(main.similarity_entry.get())

        self.setup.saving_dialogs_to_file(
            setup_path,
            checkedboxes,
            target_path,
            similarity
        )

    def reset_to_default_DIALOGS(self):
        setup_path = self.setup.DEFAULTS_DIALOGS_path

        if not os.path.exists(setup_path):

            self.setup.create_DIALOGS_setup_file()

        config = self.setup.read_config_file(setup_path)
        self.dialogs_set_setup(config)

    def reset_default_DIALOGS(self):
        setup_path = self.setup.DEFAULTS_DIALOGS_path

        self.setup.create_DIALOGS_setup_file()

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
