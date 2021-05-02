import sys

valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
similarity = 0.8


def set_app_path():

    # https://stackoverflow.com/a/404750/12490791
    program_name = sys.argv[0]

    if getattr(sys, 'frozen', False) or program_name.endswith("__main__.py"):
        application_path = ""  # relative ./
    elif __file__:
        application_path = f"{program_name}/"
    else:
        raise IOError("no path")

    return application_path
