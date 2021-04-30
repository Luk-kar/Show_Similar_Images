# import the necessary packages
from image_match.goldberg import ImageSignature


def compare_images(path_image_A, path_image_B):

    gis = ImageSignature()

    a = gis.generate_signature(path_image_A)
    b = gis.generate_signature(path_image_B)
    diff_value = 1 - gis.normalized_distance(a, b)

    # compute the mean squared error and structural similarity
    # index for the images

    return diff_value
