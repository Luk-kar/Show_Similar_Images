import os
import sys
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config import set_app_path
from config import similarity as default_similarity
from find_similar_images import find_similar_images

from UI.CheckBar import Checkbar
from UI.EntryWithPlaceholder import EntryWithPlaceholder
from UI.helpers.open_folder import open_folder
from UI.SetupMenu import SetupMenu


class Main:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")
        master.iconbitmap(
            f"{set_app_path()}UI/assets/app.ico")

        config = ConfigParser()
        config.read(os.path.join(set_app_path(), "appData", "_DEFAULT.ini"))

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.target_path_title = tk.Label(self.frame, text="images path:")
        self.target_path_title.grid(row=0, column=0, stick="w")

        self.target_path_placeholder = "Enter your folder path..."
        self.target_path_entry = EntryWithPlaceholder(
            self.frame, self.target_path_placeholder)
        self.target_path_entry
        self.target_path_entry.grid(row=1, column=0, ipadx=200, stick="we")
        self.set_entry_value(self.target_path_entry,
                             config["MATCHING"]["images path"])

        self.img_open_folder = tk.PhotoImage(
            file=f"{set_app_path()}UI/assets/open_folder.gif")
        self.button_choose_folder = tk.Button(
            self.frame, command=self.source_btn_folder_open)
        self.button_choose_folder.config(image=self.img_open_folder)
        self.button_choose_folder.grid(
            column=1, row=1, padx=(5, 0), stick="w")

        self.extensions_title = tk.Label(self.frame, text="Extensions:")
        self.extensions_title.grid(row=2, column=0, pady=(15, 0), stick="w")

        self.extensions = [  # todo
            [".png", config["FILE TYPES"][".png"]],
            [".jpg/.jpeg", config["FILE TYPES"][".jpg/.jpeg"]],
            [".bmp", config["FILE TYPES"][".bmp"]]
        ]
        self.checkbars = Checkbar(self.frame, self.extensions)
        self.checkbars.grid(row=3, column=0, pady=(0, 15), stick="w")

        self.similarity_title = tk.Label(self.frame, text="Similarity:")
        self.similarity_title.grid(row=4, column=0, stick="w")

        self.similarity_entry = EntryWithPlaceholder(
            self.frame, "Enter value from 0.0 to 1.0")
        self.similarity_entry.grid(row=5, column=0, ipadx=10, stick="w")
        self.set_entry_value(self.similarity_entry,
                             config["MINIMAL SIMILARITY"]["value"])

        self.button1 = tk.Button(
            self.master, text='Find similar images', width=25, bg="#f5f5f5", command=self.run_matching_images)
        self.button1.grid(row=1, column=0, pady=(0, 15), padx=10, stick="we")
        self.button1.config(height=2)

        self.frame.grid(row=0, column=0)

        menubar = SetupMenu(master, self)
        master.config(menu=menubar)

    def source_btn_folder_open(self):

        self.btn_find_path(self.target_path_entry,
                           lambda: filedialog.askdirectory(
                               title="Source folder")
                           )

    def btn_find_path(self, entry, askpath):

        path = askpath()
        if path:
            self.set_entry_value(entry, path)

    def set_entry_value(self, entry, value):

        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(fg='black')

    def run_matching_images(self):

        valid_extensions = self.get_extensions()
        target_path = self.target_path_entry.get()
        similarity = self.similarity_entry.get()

        try:
            founded_images_folder = find_similar_images(
                target_path, valid_extensions, similarity)
            messagebox.showinfo(
                "Success!", f"Now look for your target directory for results!\n{target_path}")
            open_folder(founded_images_folder)
        except ValueError as e:
            messagebox.showerror("Error!", e)

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

        if entry_content != self.target_path_placeholder:
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
