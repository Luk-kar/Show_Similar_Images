import tkinter as tk
import webbrowser

from config.paths import set_app_path


class About():
    """Pop-up window displaying information about creator and project"""

    def __init__(self):
        about = tk.Toplevel()
        about.title("About")
        about.iconbitmap(
            f"{set_app_path()}UI/assets/info.ico")

        # main window
        pad_value = 20
        padding = tk.Frame(about, padx=pad_value, pady=pad_value)
        padding.pack()

        # consts
        justify = "w"
        y_space = (15, 0)
        width = (0, 150)
        label_font = 'Helvetica 9 bold'

        # Version
        numb = "1.0.0"
        version_label = tk.Label(padding, text="Version:", font=label_font)
        version_label.pack(anchor=justify, padx=width)
        version_numb = tk.Label(padding, text=f"{numb}")
        version_numb.pack(anchor=justify)

        # Licence
        _type = "MIT"
        license_label = tk.Label(padding, text="License:", font=label_font)
        license_label.pack(pady=y_space, anchor=justify)
        license_type = tk.Label(padding, text=f"{_type}")
        license_type.pack(anchor=justify)
        license_link = tk.Label(padding, text="license link",
                                fg="blue", cursor="hand2")
        license_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences/blob/master/docs/LICENSE"))
        license_link.pack(anchor=justify)

        # Project type
        project_label = tk.Label(padding,
                                 text="Project site:", font=label_font)
        project_label.pack(pady=y_space, anchor=justify)
        project_link = tk.Label(padding, text="GitHub link",
                                fg="blue", cursor="hand2")
        project_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences"))
        project_link.pack(anchor=justify)

        # How to contribute
        contribute_label = tk.Label(padding, text="How to contribute:",
                                    font=label_font)
        contribute_label.pack(pady=y_space, anchor=justify)
        contribute_link = tk.Label(
            padding, text="Contribute link", fg="blue", cursor="hand2")
        contribute_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences/blob/master/docs/CONTRIBUTING.md"))
        contribute_link.pack(anchor=justify)

        # Contact
        contact = "lukkarcontact@gmail.com"
        contact_label = tk.Label(padding, text="Contact:", font=label_font)
        contact_label.pack(pady=y_space, anchor=justify)
        contact_link = tk.Label(padding, text=contact,
                                fg="blue")
        contact_link.pack(anchor=justify)

    def callback(self, url):
        webbrowser.open_new(url)
