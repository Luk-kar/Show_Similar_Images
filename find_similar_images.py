import os
import win32com.client

from compare_two_images import compare_images
import config as default_values
from config.Dialogs import Dialogs
from config.Logger import Logger

SIMILAR_IMAGES_FOLDER = "_similar images"


def get_dir_output(target_path):

    if not os.path.isdir(target_path):
        target_path = os.path.dirname(target_path)

    dir_output = os.path.abspath(os.path.join(
        target_path,
        SIMILAR_IMAGES_FOLDER)
    )
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

    filename = os.path.basename(image_path)
    path_to_shortcuts = f"{dir_output}\\{filename}"

    return path_to_shortcuts


def create_dir_for_similar_images(path_to_shortcuts):

    if not os.path.isdir(path_to_shortcuts):
        os.mkdir(path_to_shortcuts)


def get_path_for_shortcut(image, path_to_shortcuts):

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


def find_similar_images(source_path, extensions_chosen, similarity, isLog, target_path):

    # print(target_path)

    extensions_possible = get_possible_extensions()

    if not os.path.exists(source_path):
        raise ValueError("Invalid folder path or file path.")
    elif not source_path:
        raise ValueError(
            "You didn't provide any path for your images or single image.")

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

    if not bool(int(isLog)) in [False, True]:
        raise ValueError(f"Invalid isLog value: {isLog}")

    if target_path is not None and target_path != "" and target_path != "Enter your target folder path...":
        # print("target path_", target_path, "_")
        if not os.path.isdir(target_path):
            raise ValueError(
                f"Invalid target images path, it's not a folder: {target_path}")

    extensions_chosen = tuple(extensions_chosen)

    if os.path.isfile(source_path):
        if source_path.endswith(tuple(extensions_possible)):
            paths_files_source = [source_path]
        else:
            raise ValueError(
                f"Invalid source image/images path, it's not a file or folder: {target_path}")

    else:
        paths_files_source = get_images_paths(source_path, extensions_chosen)

    if target_path is not None and target_path != "":
        paths_files_target = get_images_paths(target_path, extensions_chosen)
    else:
        paths_files_target = paths_files_source.copy()

    similar_images = get_similar_images(
        paths_files_source, paths_files_target, similarity)

    print("source_path", source_path)

    dir_output = get_dir_output(source_path)

    print("dir_output", dir_output)

    if isLog:
        Logger.create_log_of_similar_images(
            similar_images,
            similarity,
            dir_output,
            target_path
        )

    create_shortcuts_of_similar_images(similar_images, dir_output)

    founded_images_folder = os.path.join(
        source_path, SIMILAR_IMAGES_FOLDER)
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
