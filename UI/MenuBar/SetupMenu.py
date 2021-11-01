import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config.Dialogs import Dialogs
from UI.helpers.open_folder import open_folder


# https://stackoverflow.com/questions/31170616/how-to-access-a-method-in-one-inherited-tkinter-class-from-another-inherited-tki
class SetupMenu(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        self.window = main
        self.dialogs = Dialogs()

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

        window = self.window

        DIALOGS_path = self.dialogs.get_dialogs_path_save()

        if DIALOGS_path:
            checkedboxes = list(window.checkbars.state())
            source_path = window.source_path_entry.get()
            target_path = window.target_path_entry.get()
            similarity = float(window.similarity_entry.get())

            self.dialogs.saving_dialogs_to_file(
                DIALOGS_path,
                checkedboxes,
                source_path,
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

        setup_path = self.dialogs.get_dialogs_path_open()

        if setup_path:
            config = self.dialogs.read_config_file(setup_path)
            self.set_setup_dialogs(config)
        else:
            messagebox.showinfo(
                "Ouch!",
                "You haven't choose any file!"
            )

    def save_to_default_DIALOGS(self):

        window = self.window

        AppFolder = self.dialogs.AppData_folder_path
        DEFAULTS_folder = self.dialogs.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.dialogs.DEFAULT_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        checkedboxes = list(window.checkbars.state())
        source_path = window.source_path_entry.get()
        target_path = window.target_path_entry.get()
        similarity = float(window.similarity_entry.get())

        self.dialogs.saving_dialogs_to_file(
            DEFAULT_DIALOGS,
            checkedboxes,
            source_path,
            target_path,
            similarity
        )

    def reset_to_default_DIALOGS(self):
        AppFolder = self.dialogs.AppData_folder_path
        DEFAULTS_folder = self.dialogs.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.dialogs.DEFAULT_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        if not os.path.exists(DEFAULT_DIALOGS):
            self.dialogs.create_DEFAULT_file()

        config = self.dialogs.read_config_file(DEFAULT_DIALOGS)
        self.set_setup_dialogs(config)

    def reset_default_DIALOGS(self):
        AppFolder = self.dialogs.AppData_folder_path
        DEFAULTS_folder = self.dialogs.DEFAULTS_folder_path
        DEFAULT_DIALOGS = self.dialogs.DEFAULT_file_path

        if not os.path.isdir(AppFolder):
            os.mkdir(AppFolder)

        if not os.path.isdir(DEFAULTS_folder):
            os.mkdir(DEFAULTS_folder)

        # it will overwrite the file if it already exists
        self.dialogs.create_DEFAULT_file()

        config = self.dialogs.read_config_file(DEFAULT_DIALOGS)
        self.set_setup_dialogs(config)

    def set_setup_dialogs(self, config):

        window = self.window

        window.source_path_entry = window.entry_set(
            window.source_path_entry, self.dialogs.get_source_path(
                config)
        )

        window.target_path_entry = window.entry_set(
            window.target_path_entry, self.dialogs.get_target_path(
                config)
        )

        picks = self.dialogs.get_checked_extensions(config)
        window.checkbars.set_state(picks)

        window.similarity_entry = window.entry_set(
            window.similarity_entry, self.dialogs.get_similarity(config)
        )
