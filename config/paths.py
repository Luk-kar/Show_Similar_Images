"""
Most essentail program's paths
"""

import os
import sys


def get_AppData_folder_path():

    appData_folder = os.path.join(set_app_path(), "appData")

    if not os.path.isdir(appData_folder):
        os.mkdir(appData_folder)

    appData_folder = os.path.abspath(appData_folder)
    return appData_folder


def get_DEFAULTS_folder_path(AppData_path):

    DEFAULTS_folder_path = os.path.join(
        AppData_path,
        "_DEFAULTS"
    )
    if not os.path.isdir(DEFAULTS_folder_path):
        os.mkdir(DEFAULTS_folder_path)

    return DEFAULTS_folder_path


def set_app_path():

    # https://stackoverflow.com/a/404750/12490791
    program_name = sys.argv[0]

    if getattr(sys, 'frozen', False) or program_name.endswith("__main__.py"):
        application_path = ""  # relative ./
    elif __file__:
        application_path = '' if program_name == 'test.py' else f"{program_name}/"

    else:
        raise IOError("no path")

    return application_path
