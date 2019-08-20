#!/usr/bin/env python3
#
# Runs tests with given wavelets, threshold values and decomposition levels
# for both soft and hard thresholding on the given images
#
# For the tested wavelets see dwt.py (line 181):
# wavelets = ['bior1.1', 'bior1.3', 'rbio1.1', 'haar', 'db1', 'db4', 'coif1', 'sym2']
import dwt


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == '__main__':
    folder = 'images/'
    images = ['adventuretime.jpg', 'country.jpg', 'gray.jpeg', 'hubble2000x2000.png']
    grayscale = [False, False, True, False]
    threshold_values = [2, 20, 50, 150]
    threshold_modes = ['soft', 'hard']
    decomposition_levels = [1, 4, 9]

    for val in threshold_values:
        for mod in threshold_modes:
            for lvl in decomposition_levels:
                for gry, img in zip(grayscale, images):
                    args = Namespace(image=folder+img, wavelet='test', threshold=val,
                                     mode=mod, levels=lvl, grayscale=gry, wavelets=False, verbose=False)
                    dwt.main(args)
