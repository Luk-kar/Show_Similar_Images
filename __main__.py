import sys

from config import Dialogs as DefaultArgs
from find_similar_images import find_similar_images
from UI.MainGUIApp import MainGUIApp


def run_GUI():
    MainGUIApp()


def parse_extensions(_argv):
    return tuple(_argv.split(","))


def run_console(_argv):

    config = DefaultArgs()
    config_default = config.read_DEFAULT()

    if len(_argv) <= 2:
        valid_extensions = config.get_checked_extensions(config_default)
        arg_extensions = []
        for ext in valid_extensions:
            if ext[1]:
                arg_extensions.append(ext[0])

        arg_extensions = ",".join(arg_extensions)
        _argv.append(arg_extensions)
    else:
        _argv[2] = parse_extensions(_argv[2])

    if len(_argv) <= 3:
        similarity = config.get_similarity(config_default)
        _argv.append(similarity)
    else:
        _argv[3] = float(_argv[3])

    find_similar_images(_argv[1], _argv[2], _argv[3])


if __name__ == "__main__":

    _argv = sys.argv

    if len(_argv) == 1:
        run_GUI()
    else:
        run_console(_argv)
