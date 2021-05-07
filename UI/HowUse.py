import tkinter as tk

from config.paths import set_app_path
from UI.MenuBar.LogMenu import LogMenu


class HowUse():
    """Pop-up window displaying information about usage"""

    def __init__(self):
        how_use = tk.Toplevel()
        how_use.title("How to use")
        how_use.iconbitmap(
            f"{set_app_path()}UI/assets/info.ico")

        # main window
        pad_value = 20
        padding = tk.Frame(how_use, padx=pad_value, pady=pad_value)
        padding.pack()

        # consts
        justify = "w"
        y_space = (0, 5)
        width = (0, 150)
        label_font = 'Helvetica 9 bold'

        text = f"""
1. Choose a folder with images to compare each image to another.
2. Pick at least of one desired file extension checkbox.
3. Write similarity value between 0.0 and 1.0
4. If you want to log result, check if in Logs menu is: "{LogMenu.label_template(True)}"
6. Finally, push the "Find similar images" button to find out results.
        """
        how_to_use_label = tk.Label(
            padding, text="How to use:", font=label_font)
        how_to_use_label.pack(anchor=justify, padx=width)
        how_to_use_content = tk.Label(
            padding, text=f"{text}", justify="left")
        how_to_use_content.pack(pady=y_space)
