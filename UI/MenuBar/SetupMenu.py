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
        self.config = Config()

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

        DIALOGS_path = self.config.get_dialogs_path_save()

        if DIALOGS_path:
            checkedboxes = list(main.checkbars.state())
            target_path = main.target_path_entry.get()
            similarity = float(main.similarity_entry.get())

            self.config.saving_dialogs_to_file(
                DIALOGS_path,
                checkedboxes,
                target_path,
                similarity
            )

            messagebox.showinfo(
                "Done!",
                "You saved setup file in:"f"\n{DIALOGS_path}"
            )

        else:

            messagebox.showinfo(
                "Ouch!",
                "You haven't saved config!"
            )

    def open_DIALOGS(self):

        setup_path = self.config.get_dialogs_path_open()

        if setup_path:
            config = self.config.read_config_file(setup_path)
            self.set_setup_dialogs(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def save_to_default_DIALOGS(self):

        main = self.main

        AppFolder = self.config.AppData_folder_path
        DEFAULTS_folder = self.config.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.config.DEFAULT_DIALOGS_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        if not os.path.exists(DEFAULT_DIALOGS):
            self.config.create_DEFAULT_DIALOGS_file()

        checkedboxes = list(main.checkbars.state())
        target_path = main.target_path_entry.get()
        similarity = float(main.similarity_entry.get())

        self.config.saving_dialogs_to_file(
            DEFAULT_DIALOGS,
            checkedboxes,
            target_path,
            similarity
        )

    def reset_to_default_DIALOGS(self):
        AppFolder = self.config.AppData_folder_path
        DEFAULTS_folder = self.config.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.config.DEFAULT_DIALOGS_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        if not os.path.exists(DEFAULT_DIALOGS):
            self.config.create_DEFAULT_DIALOGS_file()

        config = self.config.read_config_file(DEFAULT_DIALOGS)
        self.set_setup_dialogs(config)

    def reset_default_DIALOGS(self):
        AppFolder = self.config.AppData_folder_path
        DEFAULTS_folder = self.config.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.config.DEFAULT_DIALOGS_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        self.config.create_DEFAULT_DIALOGS_file()

        config = self.config.read_config_file(DEFAULT_DIALOGS)
        self.set_setup_dialogs(config)

    def set_setup_dialogs(self, config):

        main = self.main

        main.target_path_entry = main.entry_set(
            main.target_path_entry, self.config.get_images_folder_path(config)
        )

        picks = self.config.get_checked_extensions(config)
        main.checkbars.set_state(picks)

        main.similarity_entry = main.entry_set(
            main.similarity_entry, self.config.get_similarity(config)
        )
