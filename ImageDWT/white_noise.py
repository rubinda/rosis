#!/usr/bin/env python3
#
# Adds white noise to the given image
#
# :author David Rubin
import cv2
import numpy as np


def read_image(file, is_gray=False):
    """Reads an image with opencv"""
    if is_gray:
        d = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    else:
        d = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    return d


def add_white_noise(image, is_gray=False):
    """Adds 20dB of white noise"""
    target_snr_db = 20
    image_data = read_image(image, is_gray)

    image_power = np.sum(np.abs(image_data) * np.abs(image_data)) / len(image_data)
    image_avg_db = 10 * np.log10(image_power)
    noise_avg_db = image_avg_db - target_snr_db
    noise_avg_power = 10 ** (noise_avg_db / 10)
    noise = np.random.normal(0, np.sqrt(noise_avg_power), (image_data.shape[0], image_data.shape[1]))

    noisy_image = []
    for channel in cv2.split(image_data):
        noisy_image.append(channel + noise)

    cv2.imwrite('images/noisy.jpg', cv2.merge(noisy_image))


if __name__ == '__main__':
    add_white_noise('images/adventuretime.jpg', is_gray=False)