import tkinter as tk


class Demo1:
    def __init__(self, master):
        self.master = master
        master.title("Find similar images")
        master.geometry("400x400")

        self.frame = tk.Frame(self.master, padx=10, pady=15)

        self.title = tk.Label(
            self.frame, text="Target images")
        self.title.grid(column=0, row=0)

        self.target_path_entry = tk.Entry(self.frame)
        self.target_path_entry.grid(column=0, row=1)

        self.button1 = tk.Button(
            self.frame, text='New Window', width=25, command=self.new_window)
        self.button1.grid(column=0, row=2)
        self.frame.grid()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(
            self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def MainGUIApp():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()
