import tkinter as tk


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
