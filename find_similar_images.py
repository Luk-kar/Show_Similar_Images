import os
import win32com.client

from compare_two_images import compare_images
import config as default_values
from config.Dialogs import Dialogs
from config.Logger import Logger

SIMILAR_IMAGES_FOLDER = "_similar images"


def get_dir_output(target_path):

    dir_output = os.path.abspath(os.path.join(
        target_path, SIMILAR_IMAGES_FOLDER))
    if not os.path.isdir(dir_output):
        os.mkdir(dir_output)

    return dir_output


def get_images_paths(target_path, valid_extensions):
    paths_files_source = []

    for path, directories, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(valid_extensions):
                abspath = os.path.abspath(f"{target_path}\{filename}")
                paths_files_source.append(abspath)

    return paths_files_source


def init_similar_images(paths_files_source):
    similar_images = {}
    for source_path_file in paths_files_source:
        similar_images[source_path_file] = []

    return similar_images


def get_similar_images(paths_files_source, paths_files_target, similarity_desired):

    similar_images = init_similar_images(paths_files_source)

    for source_path_file in paths_files_source:
        for target_path_file in paths_files_target:
            similarity_computed = compare_images(
                source_path_file, target_path_file)
            if similarity_computed > similarity_desired:
                similar_images[source_path_file].append(target_path_file)
                paths_files_source.remove(target_path_file)

    return similar_images


def get_dir_path(image_path, dir_output):

    filename = os.path.basename(image_path)
    dir_name = os.path.splitext(filename)[0]
    path_to_shortcuts = f"{dir_output}\\{dir_name}"

    return path_to_shortcuts


def create_dir_for_similar_images(path_to_shortcuts):

    if not os.path.isdir(path_to_shortcuts):
        os.mkdir(path_to_shortcuts)


def get_path_for_shortcut(image, path_to_shortcuts):

    image_file = os.path.basename(image)
    image_name = os.path.splitext(image_file)[0]
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

    head, tail = os.path.split(path)
    file_name, ext = os.path.splitext(tail)

    file_name = file_name.rsplit('\\', 1)[-1]
    containing_folder_name = head.rsplit('\\', 1)[-1]

    if file_name == containing_folder_name:
        path = f"{head}\\_{tail}"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = image
    shortcut.WindowStyle = 3
    shortcut.save()


def find_similar_images(target_path, extensions_chosen, similarity, isLog):

    extensions_possible = get_possible_extensions()

    if not os.path.isdir(target_path):
        raise ValueError("Invalid folder path.")
    elif not target_path:
        raise ValueError("You didn't provide any path for your images.")

    extensions_chosen = extensions_chosen.split(",")
    if len(extensions_chosen) == 0:
        raise ValueError(
            f"No provided extensions: {extensions_possible}")
    else:
        for ext in extensions_chosen:
            if ext not in extensions_possible:
                raise ValueError(
                    f"Extension {ext} is invalid.\n Look at: {extensions_possible}.")

    similarity_error_message = "Invalid value, it should be between 0.0 and 1.0."
    try:
        similarity = float(similarity)
    except ValueError:
        raise ValueError(similarity_error_message)
    if not isinstance(similarity, float) or (float(similarity) < 0 or float(similarity) > 1):
        raise ValueError(similarity_error_message)

    extensions_chosen = tuple(extensions_chosen)

    paths_files_source = get_images_paths(target_path, extensions_chosen)

    paths_files_target = paths_files_source.copy()

    similar_images = get_similar_images(
        paths_files_source, paths_files_target, similarity)

    dir_output = get_dir_output(target_path)

    if isLog:
        Logger.create_log_of_similar_images(
            similar_images, similarity, dir_output)

    create_shortcuts_of_similar_images(similar_images, dir_output)

    founded_images_folder = os.path.join(
        target_path, SIMILAR_IMAGES_FOLDER)
    return founded_images_folder


def get_possible_extensions():

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
