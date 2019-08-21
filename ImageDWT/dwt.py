#!/usr/bin/env python3
#
# Program za stiskanje in ciscenje slik s pomocjo DWT (Discrete Wavelet Transform)
# Za vec podrobnosti glej porocilo.pdf
# @author David Rubin
import os
import cv2
import sys
import csv
import pywt
import argparse
import itertools
import numpy as np
from scipy.stats import pearsonr

_args = None


def calc_nrmse(x, y):
    """Returns the normalized RMSE between x and y"""
    if _args.verbose:
        print('Calculating NRMSE ...', end='')
    rmse = np.sqrt(((x - y) ** 2).mean())
    observed_mean = np.mean(y)
    if _args.verbose:
        print(' done.')
    return rmse/observed_mean


def test_wavelets(image_file, thresholds, dec_levels, threshold_modes, wavelets):
    """Test the given parameters on the image"""
    # Holds the metrics for each wavelet, threshold, mode and dec_levels combination
    metrics = []
    params = [thresholds, dec_levels, threshold_modes, wavelets]
    i = 0
    print('\n>{}'.format(image_file))
    for test_case in list(itertools.product(*params)):
        i += 1
        th, dl, tm, wav = test_case
        print('\tTesting {}:\tT:{}\tL:{}\tM:{}'.format(wav, th, dl, tm))
        _pr, _r, _cr = _test_wavelet(image_file, wav, th, dl, tm)
        metrics.append({'wavelet': wav, 'pearson correlation': _pr, 'nrmse': _r, 'compression ratio': _cr,
                        'mode': tm, 'threshold': th, 'levels': dl})
    print('Tested {} combinations'.format(i))
    # Write the metrics into a csv file
    csv_file, _ = os.path.splitext(image_file)
    csv_file = csv_file.split('/')[-1]
    write_metrics(metrics, '{}_metrics.csv'.format(csv_file))


def _test_wavelet(img, wav, tval, tlev, tmode):
    """Calculates all the metrics on a given wavelet"""
    img_dat = read_image(img, _args.grayscale)
    den_img = []
    for channel in cv2.split(img_dat):
        # Izvedi 2D DWT nad barvnim kanalom
        dwt_data = dwt(channel, wav, dl=tlev)

        # Izvedi pragovno odstranjevanje motenj
        denoised_data = threshold(dwt_data, tval, mode=tmode)

        # Pretvori obdelan kanal z iDWT in ga shrani
        den_img.append(idwt(denoised_data, wav))

    # V kolikor je vec kanalov (ni grayscale) jih zdruzi v sliko
    if len(den_img) > 1:
        new_image = cv2.merge(den_img)
    else:
        new_image = den_img[0]
    n_f = save_image(img, new_image)
    _cr = calc_compression(img, n_f)
    _pr = pearson(img_dat, new_image)
    _r = calc_nrmse(img_dat.ravel(), new_image.ravel())
    return _pr, _r, _cr


def read_image(file, is_gray=False):
    """Reads an image with opencv"""
    if _args.verbose:
        print('Reading image <{}>...'.format(file), end='')
    if is_gray:
        d = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    else:
        d = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    if _args.verbose:
        print(' done.')
    return d


def save_image(orig_file, data):
    """Saves the image into a new file with _new"""
    file_new = '{}_new.{}'.format(orig_file.split('.')[0], orig_file.split('.')[1])
    if _args.verbose:
        print('Writing image <{}> ...'.format(file_new), end='')
    cv2.imwrite(file_new, data)
    if _args.verbose:
        print(' done.')
    return file_new


def dwt(data, wav, dl=1):
    """Runs DWT one the give image with the provided wavelet and optional levels"""
    if _args.verbose:
        print('DWT ...', end='')
    d = pywt.wavedec2(data, wavelet=wav, level=dl)
    if _args.verbose:
        print(' done.')
    return d


def idwt(data, wav, dl=1):
    """Reconstruct the image (inverse DWT)"""
    if _args.verbose:
        print('Reconstrucing image (iDWT) ...', end='')
    d = pywt.waverec2(data, wav)
    if _args.verbose:
        print(' done.')
    return d


def threshold(data, value, mode='hard'):
    """Soft or hard threshold the data"""
    if _args.verbose:
        print('Thresholding ...', end='')
    d = list(map(lambda x: pywt.threshold(x, value, mode=mode), data))
    if _args.verbose:
        print(' done.')
    return d


def pearson(original, modified):
    """Calculates the Pearson correlation between the given data"""
    if _args.verbose:
        print('Calculating Pearson correlation ...', end='')
    r, _ = pearsonr(original.flat, modified.flat)
    if _args.verbose:
        print(' done.')
    return r


def calc_compression(orig, new):
    """Calculates the compression ratio"""
    return os.path.getsize(orig) / os.path.getsize(new)


def print_metrics(pear, rms, cr, new_img, tval, tmode, dec_lev, wav):
    """ Displays Pearson correlation, NRMSE value and compression ratio"""
    # Izracunaj razmerje stiskanja
    print('\n> {}'.format(new_img))
    print(' Wavelet:\t\t{}'.format(wav))
    print(' Threshold value:\t\t{:.2f}'.format(tval))
    print(' Threshold mode:\t\t{}'.format(tmode))
    print(' Decomposition level:\t{}'.format(dec_lev))
    print(' Pearson correlation:\t{:.4f}'.format(pear))
    print(' Normalized RMSE:\t\t{:.4f}'.format(rms))
    print(' Compression ratio:\t\t{:.4f}'.format(cr))


def write_metrics(metrics, filename):
    """Writes the metrics dict into the file"""
    with open('metrics/{}'.format(filename), mode='w+') as f:
        writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
        writer.writeheader()
        writer.writerows(metrics)


def main(args):
    # Dirty solution
    global _args
    _args = args
    # Parametri pri stiskanju in odstranjevanju suma
    threshold_value = args.threshold
    threshold_mode = args.mode
    dec_level = args.levels

    if not os.path.isfile(args.image):
        print('Given file <{}> does not exist!'.format(args.image))
        sys.exit(1)

    if args.wavelets:
        print('Available wavelets:')
        print(pywt.wavelist(kind='discrete'))

    image_file = args.image
    if args.wavelet == 'test':
        # Test some discrete wavelets in pywt (dmey excluded because memory error?)
        wavelets = ['bior1.3', 'haar', 'db4', 'coif1', 'sym2']
        test_wavelets(image_file, threshold_value, dec_level, threshold_mode, wavelets)
    else:
        # Preberi sliko s pomocjo opencv
        image_data = read_image(image_file, args.grayscale)
        wavelet = pywt.Wavelet(args.wavelet)
        # V kolikor levels ni podan uporabi pywt max level funkcijo
        dec_level = int(args.levels) if args.levels else pywt.dwtn_max_level(image_data[0].shape, wavelet)
        # Sliko razdeli v kanale (grayscale ima le enega) in obdelaj vsak kanal
        # Note: opencv po privzetem prebere sliko kot BGR oz. BGRA in ne RGB
        denoised_image = []
        for channel in cv2.split(image_data):
            # Izvedi 2D DWT nad barvnim kanalom
            dwt_data = dwt(channel, wavelet, dl=dec_level)

            # Izvedi pragovno odstranjevanje motenj
            denoised_data = threshold(dwt_data, threshold_value, mode=threshold_mode)

            # Pretvori obdelan kanal z iDWT in ga shrani
            denoised_image.append(idwt(denoised_data, wavelet))

        # V kolikor je vec kanalov (ni grayscale) jih zdruzi v sliko
        if len(denoised_image) > 1:
            new_image = cv2.merge(denoised_image)
        else:
            new_image = denoised_image[0]

        # Pearson korelacija
        pr = pearson(image_data, new_image)

        # normaliziran RMSE
        r = calc_nrmse(image_data.ravel(), new_image.ravel())

        # Shrani sliko v _new
        new_file = save_image(image_file, new_image)

        # Izracunaj razmerje stiskanja
        cr = calc_compression(image_file, new_file)

        # Prikazi rezultate
        print_metrics(pr, r, cr, new_file, threshold_value, threshold_mode,
                      dec_level, wavelet)


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('image', help='path to an image (jpg or png)')
    _parser.add_argument('wavelet', help='wavelet name, e.g. "haar" or "db1", set to "all" to test for best')
    _parser.add_argument('-g', '--grayscale', help='set when using a grayscale image', action='store_true')
    _parser.add_argument('-w', '--wavelets', help='list wavelets available', action='store_true')
    _parser.add_argument('-v', '--verbose', help='output more info about current operations', action='store_true')
    _parser.add_argument('-t', '--threshold', help='threshold value', type=int, default=20)
    _parser.add_argument('-m', '--mode', help='threshold mode', choices=['soft', 'hard'], default='soft')
    _parser.add_argument('-l', '--levels', help='decomposition levels', type=int)
    _params = _parser.parse_args()

    main(_params)
