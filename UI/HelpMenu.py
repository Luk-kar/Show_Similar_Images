import tkinter as tk


class SetupMenu(tk.Menu):
    def __init__(self, master):
        self.master = master

        helpMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Setup", underline=0, menu=setupMenu)
        helpMenu.add_command(
            label="Save as", command=lambda: print("click"))

        # menu_help = tk.Menu(my_menu, tearoff=False)
        # my_menu.add_cascade(label="Help", menu=menu_help)
        # menu_help.add_command(label="How to use", command=HowUse)
        # menu_help.add_separator()
        # menu_help.add_command(label="About", command=About)
