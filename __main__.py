import sys
import os
import win32com.client

from compare_two_images import compare_images


def get_dir_output(target_path):

    dir_output = os.path.abspath(f"{target_path}\\similar images")
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


def init_similar_images():
    similar_images = {}
    for source_path_file in paths_files_source:
        similar_images[source_path_file] = []

    return similar_images


def get_similar_images(paths_files_source, paths_files_target):

    similar_images = init_similar_images()

    for source_path_file in paths_files_source:
        for target_path_file in paths_files_target:
            ssim = compare_images(source_path_file, target_path_file)
            if ssim > similarity:
                similar_images[source_path_file].append(target_path_file)

    return similar_images


def get_dir_path(image_path):

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

            path_to_shortcuts = get_dir_path(image_list)
            create_dir_for_similar_images(path_to_shortcuts)

            for image in similar_images[image_list]:

                path = get_path_for_shortcut(image, path_to_shortcuts)

                create_shortcut(path, image)


def create_shortcut(path, image):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = image
    shortcut.WindowStyle = 3
    shortcut.save()


if __name__ == "__main__":

    _argv = sys.argv

    if len(_argv) == 2:

        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
        target_path = _argv[1]
        similarity = 0.8

        paths_files_source = get_images_paths(target_path, valid_extensions)

        paths_files_target = paths_files_source.copy()

        similar_images = get_similar_images(
            paths_files_source, paths_files_target)

        dir_output = get_dir_output(target_path)

        create_shortcuts_of_similar_images(similar_images, dir_output)

    else:
        print("wrong input")
