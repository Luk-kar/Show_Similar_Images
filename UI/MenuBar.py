import tkinter as tk


from UI.SetupMenu import SetupMenu


class MenuBar(tk.Menu):
    def __init__(self, parent, main):
        tk.Menu.__init__(self, parent)

        menu = tk.Menu(parent)
        self.master.config(menu=menu)

        fileMenu = SetupMenu(menu, main)

        # editMenu = Menu_2(menu)
