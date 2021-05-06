import tkinter as tk


class LogMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        logMenu = tk.Menu(parent, tearoff=False)
        parent.add_cascade(label="Logs", underline=0, menu=logMenu)

        log_status = True
        logMenu.add_command(
            label=f"Save logs {log_status}", command=self.change_log_status)

    def change_log_status(self):
        pass

        # feedback = ""
        # if "Succes!" in feedback:
        #         messagebox.showinfo("Succes!", feedback)
        #     elif "Error!" in feedback:
        #         messagebox.showerror("Error!", feedback)
        #     else:
        #         raise ValueError(f"Not valid feedback\n{feedback}")
