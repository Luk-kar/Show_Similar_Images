import tkinter as tk

from UI.About import About
from UI.HowUse import HowUse


class HelpMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        helpMenu = tk.Menu(parent, tearoff=False)
        parent.add_cascade(label="Help", underline=0, menu=helpMenu)
        helpMenu.add_command(label="How to use", command=HowUse)
        helpMenu.add_separator()
        helpMenu.add_command(label="About", command=About)
