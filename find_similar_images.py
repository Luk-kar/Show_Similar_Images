"""
This module create log of list of similar images and also shortcutes to them.
Main function returns dir path in which are contained lists of similar images
"""

import os
import win32com.client

from compare_two_images import compare_images
from config.Dialogs import Dialogs
from config.Logger import Logger

SIMILAR_IMAGES_FOLDER = "_similar images"


def get_dir_output(target_path):
    """Return string absolute path"""

    if not os.path.isdir(target_path):
        target_path = os.path.dirname(target_path)

    dir_output = os.path.abspath(
        os.path.join(
            target_path,
            SIMILAR_IMAGES_FOLDER
        )
    )
    if not os.path.isdir(dir_output):
        os.mkdir(dir_output)

    return dir_output


def get_images_paths(target_path, valid_extensions):
    """Get all absolute paths in given directory"""

    paths_files_source = []

    for path, directories, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(valid_extensions):
                abspath = os.path.abspath(f"{target_path}\\{filename}")
                paths_files_source.append(abspath)

    return paths_files_source


def init_similar_images(paths_files_source):
    """Return empty dictionary of lists, where keys are names of source images"""

    similar_images = {}
    for source_path_file in paths_files_source:
        similar_images[source_path_file] = []

    return similar_images


def get_similar_images(paths_files_source, paths_files_target, similarity_desired):
    """Return populated dictionary of lists of paths of matched images"""

    similar_images = init_similar_images(paths_files_source)

    if paths_files_source == paths_files_target:

        for source_path_file in paths_files_source:

            for target_path_file in paths_files_target:

                similarity_computed = compare_images(
                    source_path_file, target_path_file)

                if similarity_computed >= similarity_desired:

                    similar_images[source_path_file].append(target_path_file)
                    paths_files_source.remove(target_path_file)

    else:

        for source_path_file in paths_files_source:

            similar_images[source_path_file].append(source_path_file)

            for target_path_file in paths_files_target:

                similarity_computed = compare_images(
                    source_path_file, target_path_file)

                if similarity_computed >= similarity_desired:
                    similar_images[source_path_file].append(target_path_file)
                    paths_files_target.remove(target_path_file)

    return similar_images


def get_dir_path(image_path, dir_output):
    """Get dir with dirs, witch will be populated by shortcuts"""

    filename = os.path.basename(image_path)
    path_to_shortcuts = f"{dir_output}\\{filename}"

    return path_to_shortcuts


def create_dir_for_similar_images(path_to_shortcuts):
    """Create dir if not exists"""

    if not os.path.isdir(path_to_shortcuts):
        os.mkdir(path_to_shortcuts)


def get_path_for_shortcut(image, path_to_shortcuts):
    """Return string path"""

    image_name = os.path.basename(image)
    path = os.path.join(path_to_shortcuts, f'{image_name}.lnk')

    return path


def create_shortcuts_of_similar_images(similar_images, dir_output):

    for image_list in similar_images:

        if len(similar_images[image_list]) > 1:

            path_to_shortcuts = get_dir_path(image_list, dir_output)
            create_dir_for_similar_images(path_to_shortcuts)

            for image in similar_images[image_list]:

                path = get_path_for_shortcut(image, path_to_shortcuts)

                create_shortcut(path, image)


def create_shortcut(path, image):
    """Windows OS crete shortcut"""

    head, tail = os.path.split(path)
    file_name, ext = os.path.splitext(tail)

    file_name = file_name.rsplit('\\', 1)[-1]
    containing_folder_name = head.rsplit('\\', 1)[-1]

    # To show source reference image as first
    if file_name == containing_folder_name:
        tail = f"_{tail}"
        path = os.path.join(head, tail)

        # To avoid situation when, you have the same file name in source folder and target folder
        if os.path.exists(path):
            tail = f"{file_name}{ext}"
            path = os.path.join(head, tail)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = image
    shortcut.WindowStyle = 3
    shortcut.save()


def find_similar_images(source_path, extensions_chosen, similarity, is_log, target_path):
    """Main module function. It creates log and dirs with shortcutes to similar images"""

    extensions_possible = get_possible_extensions()

    check_if_path_exists(source_path)

    extensions_chosen = get_list_extensions(extensions_chosen)
    check_if_extensions_are_valid(extensions_chosen, extensions_possible)

    similarity = check_if_similarity_is_valid(similarity)

    check_if_is_log_valid(is_log)

    check_if_target_dir_is_valid(target_path)

    paths_files_source = get_paths_images_source(
        source_path, extensions_possible, extensions_chosen)

    paths_files_target = get_paths_images_target(
        target_path, extensions_chosen, paths_files_source)

    similar_images = get_similar_images(
        paths_files_source, paths_files_target, similarity)

    founded_images_folder = get_dir_output(source_path)

    if is_log:
        Logger.create_log_of_similar_images(
            similar_images,
            similarity,
            founded_images_folder,
            source_path,
            target_path
        )

    create_shortcuts_of_similar_images(similar_images, founded_images_folder)

    return founded_images_folder


def get_list_extensions(extensions_chosen):
    return extensions_chosen.split(",")


def check_if_similarity_is_valid(similarity):
    """Raise error if not true"""

    similarity_error_message = "Invalid value, it should be between 0.0 and 1.0."
    try:
        similarity = float(similarity)
    except ValueError:
        raise ValueError(similarity_error_message)
    if not isinstance(similarity, float) or (float(similarity) < 0 or float(similarity) > 1):
        raise ValueError(similarity_error_message)
    return similarity


def check_if_path_exists(source_path):
    """Raise error if not true"""

    if not os.path.exists(source_path):
        raise ValueError("Invalid folder path or file path.")
    elif not source_path:
        raise ValueError(
            "You didn't provide any path for your images or single image.")


def check_if_extensions_are_valid(extensions, extensions_possible):
    """Raise error if not true"""

    if len(extensions) == 0:
        raise ValueError(
            f"No provided extensions: {extensions_possible}")
    else:
        for ext in extensions:
            if ext not in extensions_possible:
                raise ValueError(
                    f"Extension {ext} is invalid.\n Look at: {extensions_possible}.")


def check_if_is_log_valid(is_log):
    """Raise error if not true"""

    if not bool(int(is_log)) in [False, True]:
        raise ValueError(f"Invalid isLog value: {is_log}")


def check_if_target_dir_is_valid(target_path):
    """Raise error if not true"""

    if target_path is not None and target_path != "" and target_path != "Enter your target folder path... (Optional)":
        if not os.path.isdir(target_path):
            raise ValueError(
                f"Invalid target images path, it's not a folder: {target_path}")


def get_paths_images_source(source_path, extensions_possible, extensions_chosen):
    """Raise error if not true"""

    extensions_chosen = tuple(extensions_chosen)

    if os.path.isfile(source_path):
        if source_path.endswith(tuple(extensions_possible)):
            return [source_path]
        else:
            raise ValueError(
                f"Invalid source image/images path, it's not a file or folder: {source_path}")

    else:
        return get_images_paths(source_path, extensions_chosen)


def get_paths_images_target(target_path, extensions_chosen, paths_files_source):
    """Raise error if not true"""

    extensions_chosen = tuple(extensions_chosen)

    if target_path is not None and target_path != "":
        paths_files_target = get_images_paths(target_path, extensions_chosen)
    else:
        paths_files_target = paths_files_source.copy()
    return paths_files_target


def get_possible_extensions():
    """Get all valid extensions from config file"""

    config = Dialogs()
    config_DEFAULT = config.get_DEFAULT()

    extensions_default = []
    extensions = config.get_checked_extensions(config_DEFAULT)
    for ext in extensions:
        if "/" in ext[0]:  # mutli extensions type like .jpg/.jpeg
            extensions = ext[0].split("/")
            extensions_default += extensions
        else:
            extensions_default.append(ext[0])

    return extensions_default
