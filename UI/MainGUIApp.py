import tkinter as tk
from tkinter import filedialog  # for Python 3
from tkinter import messagebox

from find_similar_images import find_similar_images
from config import set_app_path


class Demo1:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.target_path_title = tk.Label(self.frame, text="Target images:")
        self.target_path_title.grid(row=0, column=0, stick="w")

        self.target_path_entry = tk.Entry(self.frame)
        self.target_path_entry.grid(row=1, column=0, stick="we")

        self.img_open_folder = tk.PhotoImage(
            file=f"{set_app_path()}UI/assets/open_folder.gif")
        self.button_choose_folder = tk.Button(
            self.frame, command=self.source_btn_folder_open)
        self.button_choose_folder.config(image=self.img_open_folder)
        self.button_choose_folder.grid(
            column=1, row=1, pady=(0, 5), stick="w")

        self.extensions = [".png", ".jpg/.jpeg", ".bmp"]
        self.checkbars = Checkbar(self.frame, self.extensions)
        self.checkbars.grid(row=2, column=0, pady=10)

        self.similarity_title = tk.Label(self.frame, text="Similarity:")
        self.similarity_title.grid(row=3, column=0, stick="w")

        self.similarity_entry = tk.Entry(self.frame)
        self.similarity_entry.grid(row=4, column=0, stick="w")

        self.button1 = tk.Button(
            self.master, text='Find similar images', width=25, command=self.run_matching_images)
        self.button1.grid(row=1, column=0, pady=(0, 15), padx=10, stick="we")
        self.frame.grid(row=0, column=0)

    def source_btn_folder_open(self):

        self.btn_find_path(self.target_path_entry,
                           lambda: filedialog.askdirectory(
                               title="Source folder")
                           )

    def btn_find_path(self, entry, askpath):

        path = askpath()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
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
    def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


def MainGUIApp():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()
