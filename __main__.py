import sys
import os

from compare_two_images import compare_images

_argv = sys.argv

if len(_argv) == 2:

    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
    paths_files_source = []

    for path, directories, files in os.walk(_argv[1]):
        for filename in files:
            if filename.endswith(valid_extensions):
                paths_files_source.append(f"{_argv[1]}\{filename}")

    paths_files_target = paths_files_source.copy()

    similar_images = {}

    for source_path_file in paths_files_source:
        similar_images[source_path_file] = []

    for source_path_file in paths_files_source:
        for target_path_file in paths_files_target:
            ssim = compare_images(source_path_file, target_path_file)
            if ssim > 0.8 and target_path_file != source_path_file:
                similar_images[source_path_file].append(target_path_file)
                # paths_files_target.remove(target_path_file)

    print(similar_images)

else:
    print("wrong input")
