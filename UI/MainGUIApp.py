import tkinter as tk

from find_similar_images import find_similar_images
from tkinter import messagebox


class Demo1:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")
        master.geometry("400x400")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.target_path_title = tk.Label(self.frame, text="Target images")
        self.target_path_title.grid(column=0, row=0)

        self.target_path_entry = tk.Entry(self.frame)
        self.target_path_entry.grid(column=0, row=1)

        self.extensions = [".png", ".jpg/.jpeg", ".bmp"]
        self.checkbars = Checkbar(self.frame, self.extensions)
        self.checkbars.grid(column=0, row=2)

        self.similarity_title = tk.Label(self.frame, text="Similarity")
        self.similarity_title.grid(column=0, row=3)

        self.similarity_entry = tk.Entry(self.frame)
        self.similarity_entry.grid(column=0, row=4)

        self.button1 = tk.Button(
            self.frame, text='Find similar images', width=25, command=self.new_window)
        self.button1.grid(column=0, row=5)
        self.frame.grid()

    def new_window(self):

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
