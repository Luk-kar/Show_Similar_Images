# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def compare_images(path_image_A, path_image_B):

    imageA = cv2.imread(path_image_A)
    imageB = cv2.imread(path_image_B)

    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the mean squared error and structural similarity
    # index for the images
    return ssim(imageA, imageB)
