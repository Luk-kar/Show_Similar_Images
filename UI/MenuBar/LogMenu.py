import tkinter as tk
import os

from config.Logger import Logger


class LogMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        self.logger = Logger()
        label = self.get_label()

        self.logMenu = tk.Menu(parent, tearoff=False)
        parent.add_cascade(label="Logs", underline=0, menu=self.logMenu)

        self.logMenu.add_command(
            label=label, command=self.change_log_status)

    def change_log_status(self):
        is_writing = self.logger.read_writing_status()
        negation = int(not is_writing)
        self.logger.set_writing_status(negation)

        label = self.label_template(str(bool(negation)))

        self.logMenu.entryconfigure(1, label=label)

    def get_label(self):
        boolean = bool(self.logger.read_writing_status())
        return self.label_template(boolean)

    def label_template(self, boolean):
        return f"Save logs: {boolean}"
