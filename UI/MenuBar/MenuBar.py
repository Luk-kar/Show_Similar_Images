import tkinter as tk


from .SetupMenu import SetupMenu
from .LogMenu import LogMenu
from .HelpMenu import HelpMenu


class MenuBar(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        menu = tk.Menu(parent)
        self.master.config(menu=menu)

        setupMenu = SetupMenu(menu, main)

        logMenu = LogMenu(menu)

        helpMenu = HelpMenu(menu)
