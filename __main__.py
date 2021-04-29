import sys
import os

from compare_two_images import compare_images

_argv = sys.argv

if len(_argv) == 2:

    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
    paths_files_source = []
    target_path = _argv[1]
    similar_images = {}

    for path, directories, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(valid_extensions):
                paths_files_source.append(f"{target_path}\{filename}")

    paths_files_target = paths_files_source.copy()

    for source_path_file in paths_files_source:
        similar_images[source_path_file] = []

    for source_path_file in paths_files_source:
        for target_path_file in paths_files_target:
            ssim = compare_images(source_path_file, target_path_file)
            if ssim > 0.8 and target_path_file != source_path_file:
                similar_images[source_path_file].append(target_path_file)

    # for image in similar_images:
    dir_output = f"{target_path}\\similar images"
    if not os.path.isdir(dir_output):
        os.mkdir(dir_output)

    for i in similar_images:
        if similar_images[i] != []:
            filename = os.path.basename(i)
            dir_name = os.path.splitext(filename)[0]
            path_to_shortcuts = f"{dir_output}\\{dir_name}"

            if not os.path.isdir(path_to_shortcuts):
                os.mkdir(path_to_shortcuts)

            for image in similar_images[i]:
                image_file = os.path.basename(image)
                image_name = os.path.splitext(image_file)[0]
                path = os.path.join(path_to_shortcuts, f'{image_name}.lnk')
                print(path)

else:
    print("wrong input")
