import tkinter as tk
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from find_similar_images import find_similar_images
from config import set_app_path, similarity as default_similarity


class Demo1:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")
        master.iconbitmap(
            f"{set_app_path()}UI/assets/app.ico")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.target_path_title = tk.Label(self.frame, text="Images path:")
        self.target_path_title.grid(row=0, column=0, stick="w")

        self.target_path_entry = EntryWithPlaceholder(
            self.frame, "Enter your folder path...")
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

        self.extensions = [".png", ".jpg/.jpeg", ".bmp"]
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

        extensions_to_use = []
        checkedboxes = list(self.checkbars.state())
        for count, box in enumerate(checkedboxes):
            if box == 1:
                extensions_to_use.append(self.extensions[count])

        target_path = self.target_path_entry.get()
        valid_extensions = ",".join(extensions_to_use).replace("/", ",")
        similarity = float(self.similarity_entry.get())

        try:
            find_similar_images(target_path, valid_extensions, similarity)
            messagebox.showinfo(
                "Succes!", f"Now look for your target directory for results!\n{target_path}")
            # open folder todo
        except ValueError as e:
            messagebox.showerror("Error!", e)


class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=[], side="left", anchor="w"):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


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
    app = Demo1(root)
    root.mainloop()
