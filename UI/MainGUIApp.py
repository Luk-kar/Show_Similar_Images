import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config.Dialogs import Dialogs
from config.paths import set_app_path
from config.Logger import Logger
from find_similar_images import find_similar_images

from .CheckBar import Checkbar
from .EntryWithPlaceholder import EntryWithPlaceholder
from .helpers.open_folder import open_folder
from .MenuBar.MenuBar import MenuBar


class Main:
    def __init__(self, master):
        self.master = master

        # upload data
        config = Dialogs()
        config_DEFAULT = config.get_DEFAULT()

        # create frame
        master.title("Find similar images")
        master.iconbitmap(
            f"{set_app_path()}UI/assets/app.ico")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        # source entry
        entry_width = 300

        # source title
        self.source_path_title = tk.Label(
            self.frame, text="Source images path:")
        self.source_path_title.grid(row=0, column=0, stick="w")

        # source entry
        self.source_placeholder = "Enter your source folder or file path..."
        self.source_path_entry = EntryWithPlaceholder(
            self.frame, self.source_placeholder)
        self.source_path_entry.grid(
            row=1, column=0, ipadx=entry_width, stick="we")
        self.set_entry_value(self.source_path_entry,
                             config.get_source_path(config_DEFAULT))

        # source open folder
        self.img_open_folder = tk.PhotoImage(
            file=f"{set_app_path()}UI/assets/open_folder.gif")
        self.button_choose_source_folder = tk.Button(
            self.frame, command=self.source_folder_open)
        self.button_choose_source_folder.config(image=self.img_open_folder)
        self.button_choose_source_folder.grid(
            column=1, row=1, padx=(5, 0), stick="w")

        # source open file
        self.img_open_file = tk.PhotoImage(
            file=f"{set_app_path()}UI/assets/open_file.gif")
        self.button_choose_source_file = tk.Button(
            self.frame, command=self.source_file_open)
        self.button_choose_source_file.config(image=self.img_open_file)
        self.button_choose_source_file.grid(
            column=2, row=1, padx=(5, 0), stick="w")

        # target title
        self.target_path_title = tk.Label(
            self.frame, text="Target images path:")
        self.target_path_title.grid(row=2, column=0, pady=(10, 0), stick="w")

        # target entry
        self.target_placeholder = "Enter your target folder path... (Optional)"
        self.target_path_entry = EntryWithPlaceholder(
            self.frame,
            self.target_placeholder
        )
        self.target_path_entry.grid(
            row=3, column=0, ipadx=entry_width, stick="we")
        self.set_entry_value(self.target_path_entry,
                             config.get_target_path(config_DEFAULT))

        # target open folder
        self.button_choose_target_folder = tk.Button(
            self.frame, command=self.target_folder_open)
        self.button_choose_target_folder.config(image=self.img_open_folder)
        self.button_choose_target_folder.grid(
            column=1, row=3, padx=(5, 0), stick="w")

        # Extensions title
        self.extensions_title = tk.Label(self.frame, text="Extensions:")
        self.extensions_title.grid(row=4, column=0, pady=(15, 0), stick="w")

        # Extensions checkbars
        self.extensions = config.get_checked_extensions(config_DEFAULT)
        self.checkbars = Checkbar(self.frame, self.extensions)
        self.checkbars.grid(row=5, column=0, pady=(0, 15), stick="w")

        # similarity title
        self.similarity_title = tk.Label(self.frame, text="Similarity:")
        self.similarity_title.grid(row=6, column=0, stick="w")

        # similarity entry
        self.similarity_entry = EntryWithPlaceholder(
            self.frame, "Enter value from 0.0 to 1.0")
        self.similarity_entry.grid(row=7, column=0, ipadx=10, stick="w")
        self.set_entry_value(self.similarity_entry,
                             config.get_similarity(config_DEFAULT))

        # Run program button
        self.button_run_program = tk.Button(
            self.master, text='Find similar images', width=25, bg="#f5f5f5", command=self.run_matching_images)
        self.button_run_program.grid(
            row=1, column=0, pady=(0, 15), padx=10, stick="we")
        self.button_run_program.config(height=2)

        self.frame.grid(row=0, column=0)

        menubar = MenuBar(self.master, self)

    def source_folder_open(self):

        self.get_folder_path(self.source_path_entry, "Source folder")

    def target_folder_open(self):

        self.get_folder_path(self.target_path_entry, "Target folder")

    def get_folder_path(self, entry, title):  # todo

        chosen_directory = self.btn_find_path(entry,
                                              lambda: filedialog.askdirectory(
                                                  title=title)
                                              )

        if chosen_directory:
            count = self.check_how_many_valid_files(chosen_directory)

            if not self.get_extensions():
                return messagebox.showwarning(
                    "Failed!", f"You did NOT choose any file extensions!")

            if count:
                messagebox.showwarning(
                    "Success!", f"There are {count} images to check in folder!")
            else:
                messagebox.showwarning(
                    "Failed!", f"There are NO, NADA, ZERO, ZINCH, 0\nimages to check in folder!")

    def source_file_open(self):

        self.get_file_path(self.source_path_entry, "Source file")

    def get_file_path(self, entry, title):
        self.btn_find_path(entry,
                           lambda: filedialog.askopenfilename(
                               title=title,
                               filetypes=[
                                   ("png files", "*.png"),
                                   ("jpg files", ("*.jpg", "*.jpeg", "*.jpe")),
                                   ("bmp files", "*.bmp")
                               ])
                           )

    def check_how_many_valid_files(self, chosen_directory):

        count = 0

        for name in os.listdir(chosen_directory):
            if name.endswith(tuple(self.get_extensions())):
                count += 1

        return count

    def btn_find_path(self, entry, askpath):

        path = askpath()
        if path:
            self.set_entry_value(entry, path)

        return path

    def set_entry_value(self, entry, value):

        if value:
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(fg='black')

    def run_matching_images(self):

        valid_extensions = self.get_extensions()
        source_path = self.source_path_entry.get()
        target_path = self.target_path_entry.get()
        similarity = self.similarity_entry.get()

        isLog = self.isLogging()

        try:
            founded_images_folder = find_similar_images(
                source_path,
                valid_extensions,
                similarity,
                isLog,
                target_path
            )
            messagebox.showinfo(
                "Success!", f"Now look for your target directory for results!\n{target_path}")
            open_folder(founded_images_folder)
        except ValueError as e:
            messagebox.showerror("Error!", e)

    def isLogging(self):

        logger = Logger()
        if not os.path.exists(logger.file_path):
            logger.create_DEFAULT_file()
        isLog = bool(logger.read_writing_status())
        return isLog

    def get_extensions(self):

        def get_checkboxes_values(self):

            extensions_to_use = []
            checkedboxes = list(self.checkbars.state())
            for count, box in enumerate(checkedboxes):
                if box == 1:
                    extensions_to_use.append(self.extensions[count])

            return extensions_to_use

        def convert_values_into_cli_arg(extensions_to_use):
            valid_extension = []
            for ext in extensions_to_use:
                valid_extension.append(ext[0])

            valid_extensions = ",".join(valid_extension).replace("/", ",")
            return valid_extensions

        extensions_to_use = get_checkboxes_values(self)

        valid_extensions = convert_values_into_cli_arg(extensions_to_use)

        return valid_extensions

    def entry_set(self, entry, entry_content):

        entry = self.entry_set_text(entry, entry_content)

        if entry_content != self.target_placeholder:
            entry.config(fg='black')
        else:
            entry.config(fg='grey')

        return entry

    def entry_set_text(self, entry, text):

        entry.delete(0, "end")
        entry.insert(
            0,
            text
        )

        return entry


def MainGUIApp():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
