"""
NAME

    Show_Images_Differences

DESCRIPTION

    Creating list of similar images
    ========================================

    Find_Similar_Images is used for to find:
    1) similar images withing particular folder
    2) similar images between folders
    3) list of similar images to particular chosen file within target folder.

    Usecase example:
    find similar images within UI assets.

    Of course, it can be used for any other matching images purposes

    This program uses image recognition algorithms from https://image-match.readthedocs.io

AUTHOR

    Karol Łukaszczyk
    e-mail: lukkarcontact@gmail.com
"""

import sys

from config.Dialogs import Dialogs as DefaultArgs
from config.Logger import Logger
from find_similar_images import find_similar_images
from UI.MainGUIApp import MainGUIApp


def run_GUI():
    """If args are not provided for program, runs GUI version"""
    MainGUIApp()


def run_console(_argv):
    """if program args provided"""

    source_path, chosen_extensions, similarity, isLog, target_path = parsing_program_args(
        _argv)

    find_similar_images(
        source_path,
        chosen_extensions,
        similarity,
        isLog,
        target_path
    )


def parsing_program_args(_argv):
    """checking if args are valid and changing args types to accurate ones"""

    config = DefaultArgs()
    config_default = config.get_DEFAULT()

    source_path = _argv[1]

    if len(_argv) <= 2:
        accepted_extensions = config.get_checked_extensions(config_default)
        chosen_extensions = []
        for ext in accepted_extensions:
            if ext[1]:
                chosen_extensions.append(ext[0])

        chosen_extensions = ",".join(chosen_extensions)
    else:
        chosen_extensions = _argv[2]

    if len(_argv) <= 3:
        similarity = config.get_similarity(config_default)
    else:
        similarity = float(_argv[3])

    if len(_argv) <= 4:
        logger = Logger()
        is_log = bool(logger.read_writing_status())
    else:
        is_log = bool(int(_argv[4]))

    if len(_argv) <= 5:
        target_path = None
    else:
        target_path = _argv[5]
    return source_path, chosen_extensions, similarity, is_log, target_path


if __name__ == "__main__":

    _argv = sys.argv

    if len(_argv) == 1:
        run_GUI()
    else:
        run_console(_argv)
