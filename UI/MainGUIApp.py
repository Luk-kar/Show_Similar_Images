from configparser import ConfigParser
import os
import sys
import tkinter as tk
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from config import set_app_path
from config import similarity as default_similarity
from find_similar_images import find_similar_images
from UI.helpers.open_folder import open_folder


class Main:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")
        master.iconbitmap(
            f"{set_app_path()}UI/assets/app.ico")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.target_path_title = tk.Label(self.frame, text="Images path:")
        self.target_path_title.grid(row=0, column=0, stick="w")

        self.target_path_placeholder = "Enter your folder path..."
        self.target_path_entry = EntryWithPlaceholder(
            self.frame, self.target_path_placeholder)
        self.target_path_entry
        self.target_path_entry.grid(row=1, column=0, ipadx=200, stick="we")

        self.img_open_folder = tk.PhotoImage(
            file=f"{set_app_path()}UI/assets/open_folder.gif")
        self.button_choose_folder = tk.Button(
            self.frame, command=self.source_btn_folder_open)
        self.button_choose_folder.config(image=self.img_open_folder)
        self.button_choose_folder.grid(
            column=1, row=1, padx=(5, 0), stick="w")

        self.extensions_title = tk.Label(self.frame, text="Extensions:")
        self.extensions_title.grid(row=2, column=0, pady=(15, 0), stick="w")

        self.extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
        self.checkbars = Checkbar(self.frame, self.extensions)
        self.checkbars.grid(row=3, column=0, pady=(0, 15), stick="w")

        self.similarity_title = tk.Label(self.frame, text="Similarity:")
        self.similarity_title.grid(row=4, column=0, stick="w")

        self.similarity_entry = EntryWithPlaceholder(
            self.frame, "Enter value from 0.0 to 1.0")
        self.similarity_entry.grid(row=5, column=0, ipadx=10, stick="w")
        self.set_entry_value(self.similarity_entry, default_similarity)

        self.button1 = tk.Button(
            self.master, text='Find similar images', width=25, bg="#f5f5f5", command=self.run_matching_images)
        self.button1.grid(row=1, column=0, pady=(0, 15), padx=10, stick="we")
        self.button1.config(height=2)

        self.frame.grid(row=0, column=0)

        menubar = MenuBar(master, self)
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
            find_similar_images(target_path, valid_extensions, similarity)
            messagebox.showinfo(
                "Success!", f"Now look for your target directory for results!\n{target_path}")
            open_folder(target_path)
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
                "You haven't choose any folder!"
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

        messagebox.showinfo(
            "Done!",
            "You saved setup file in:"f"\n{setup_path}"
        )

    def setup_reset_to_defaults(self):
        setup_file = os.path.join(self.ini_default_location, "_DEFAULT.ini")

        if not os.path.exists(setup_file):
            setup_file = os.path.join(
                self.ini_default_location, "_DEFAULT.ini")

            valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
            checkedboxes = map(lambda x: x[1], valid_extensions)
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

        if not os.path.exists(setup_file):
            setup_file = os.path.join(
                self.ini_default_location, "_DEFAULT.ini")

            valid_extensions = [[".png", 1], [".jpg/.jpeg", 0], [".bmp", 0]]
            checkedboxes = map(lambda x: x[1], valid_extensions)
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


class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=[], side="left", anchor="w"):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar(value=pick[1])
            chk = tk.Checkbutton(self, text=pick[0], variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)

    def set_state(self, picks):

        for count, pick in enumerate(picks):
            self.vars[count].set(pick[1])

        return self.vars


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def MainGUIApp():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
