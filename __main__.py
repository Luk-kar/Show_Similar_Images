import sys

from config.Dialogs import Dialogs as DefaultArgs
from config.Logger import Logger
from find_similar_images import find_similar_images
from UI.MainGUIApp import MainGUIApp


def run_GUI():
    MainGUIApp()


def parse_extensions(_argv):
    return tuple(_argv.split(","))


def run_console(_argv):

    config = DefaultArgs()
    config_default = config.get_DEFAULT()

    folder_path = _argv[1]

    if len(_argv) <= 2:
        accepted_extensions = config.get_checked_extensions(config_default)
        chosen_extensions = []
        for ext in accepted_extensions:
            if ext[1]:
                chosen_extensions.append(ext[0])

        chosen_extensions = ",".join(chosen_extensions)
    else:
        chosen_extensions = parse_extensions(_argv[2])

    if len(_argv) <= 3:
        similarity = config.get_similarity(config_default)
    else:
        similarity = float(_argv[3])

    if len(_argv) <= 4:
        logger = Logger()
        isLog = bool(logger.read_writing_status())
    else:
        isLog = bool(int(_argv[4]))

    find_similar_images(folder_path, chosen_extensions, similarity, isLog)


if __name__ == "__main__":

    _argv = sys.argv

    if len(_argv) == 1:
        run_GUI()
    else:
        run_console(_argv)
