import sys

import config as default_value
from find_similar_images import find_similar_images
from UI.MainGUIApp import MainGUIApp


def run_GUI():
    MainGUIApp()


def parse_extensions(_argv):
    return tuple(_argv.split(","))


def run_console(_argv):

    if len(_argv) <= 2:
        valid_extensions = default_value.valid_extensions
        _argv.append(valid_extensions)
    else:
        _argv[2] = parse_extensions(_argv[2])

    if len(_argv) <= 3:
        similarity = default_value.similarity
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
