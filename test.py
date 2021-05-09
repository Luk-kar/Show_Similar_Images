import unittest
import os
import shutil

from find_similar_images import find_similar_images


class TestFindSimilarImages(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFindSimilarImages, self).__init__(*args, **kwargs)

        self.chosen_images = os.path.abspath(
            os.path.join("tests", "data", "chosen images"))
        self._similar_images_path = os.path.join(
            self.chosen_images, "_similar images")

        self.args = {
            "folder path": self.chosen_images,
            "extensions": [".png", "jpg.", "jpeg.", "bmp."],
            "similarity": [0.0, 0.5, 0.8, 1.0],
            "isLog": [0, 1]
        }

        images_names = [
            "black_bg.png",
            "changed.png",
            "diff_size.png",
            "same 001.png",
            "same 002.png",
            "white_bg.png",
            "white_bg_with_black_sq.png"
        ]

        self.images = self.create_dict_same_keys_values(images_names)

    def create_dict_same_keys_values(self, images_names):

        images = {}

        for key in images_names:
            images[key] = key

        return images

    def change_extensions_list_to_string(self, extensions):
        return ",".join(extensions)

    def setUp(self):
        if self.similar_images_folder_exists():
            shutil.rmtree(self._similar_images_path)

    # def tearDown(self):
    #     print("tearDown")

    # @classmethod
    # def tearDownClass(cls):
    #     print("tearDownClass")

    # @classmethod
    # def setUpClass(cls):
    #     print("setUpClass")

    def log_find_path(self):

        directory = self._similar_images_path

        for name in os.listdir(directory):
            if name.endswith("-list.log"):
                return os.path.join(directory, name)

        return None

    def log_exists(self):

        for name in os.listdir(self._similar_images_path):
            if name.endswith("-list.log"):
                return True

        return False

    def log_is_correct(self, directory, similarity, file_names):

        file_path = self.log_find_path()
        file_log = open(file_path, "r")
        content = file_log.read()
        file_log.close()

        if not directory in content:
            return False

        if not str(similarity) in content:
            return False

        for file_name in file_names:
            if not file_name in content:
                return False

        return True

    def similar_images_folder_exists(self):
        return os.path.isdir(self._similar_images_path)

    def files_in_folder_exists(self, founded_images):

        def get_no_extension(filename):
            return filename.rsplit(".", 1)[0]

        directory = self._similar_images_path
        existing_files = []

        for path, dirs, files in os.walk(directory):
            for f in files:
                if not f.endswith('.log'):
                    no_ext = get_no_extension(f)
                    if no_ext[0] == "_":
                        no_ext = no_ext[1:]
                    existing_files.append(no_ext)

        for count, found in enumerate(founded_images):
            founded_images[count] = get_no_extension(found)

        print(sorted(founded_images))
        print(sorted(existing_files))

        return sorted(founded_images) == sorted(existing_files)

    def test_png_08_isLog(self):

        image_folder = self.args["folder path"]

        extensions = self.args["extensions"][0]

        similarity = self.args["similarity"][2]

        isLog = self.args["isLog"][1]

        find_similar_images(image_folder, extensions, similarity, isLog)

        self.assertTrue(
            self.similar_images_folder_exists(),
            f"folder was not created:\n{self._similar_images_path}"
        )

        self.assertTrue(
            self.log_exists(),
            "log file was not created"
        )

        founded_images = [
            self.images["diff_size.png"],
            self.images["same 001.png"],
            self.images["same 002.png"],
            self.images["white_bg.png"]
        ]

        self.assertTrue(
            self.log_is_correct(image_folder, similarity, founded_images),
            "The log is corrupted "
        )

        self.assertTrue(
            self.files_in_folder_exists(founded_images),
            "Founded files are not correct"
        )


if __name__ == "__main__":
    unittest.main()
