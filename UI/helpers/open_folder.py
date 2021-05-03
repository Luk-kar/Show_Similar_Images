import os
import platform
import subprocess


def open_folder(path):
    """open folder in file explorer, depending on platfrom"""

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
