#!/usr/bin/env python3
#
# Program za stiskanje in ciscenje slik s pomocjo DWT (Discrete Wavelet Transform)
# Za vec podrobnosti glej porocilo.pdf
# @author David Rubin
import pywt
import cv2
import os
import sys
import csv
import argparse
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


def test_wavelets(img, tval, tlev, tmode, wavs):
    """Test all possible wavelets and return top 3"""
    wavelets = wavs
    # Holds the metrics for each wavelet in format
    # metrics[<wavelet>] = (<pearson corr.>, <nrmse>, <compression ratio>)
    metrics = []
    print('\n>{}\tTH:{} TM:{} DL:{}'.format(img, tval, tmode, tlev))
    for i, wav in enumerate(wavelets):
        print('\tTesting {} ({}/{})'.format(wav, i+1, len(wavelets)))
        _pr, _r, _cr = _test_wavelet(img, wav, tval, tlev, tmode)
        metrics.append({'wavelet': wav, 'pearson correlation': _pr, 'nrmse': _r, 'compression ratio': _cr})
    # Write the metrics into a csv file
    csv_file, _ = os.path.splitext(img)
    csv_file = csv_file.split('/')[-1]
    write_metrics(metrics, '{}_{}_{}_{}.csv'.format(csv_file, tval, tmode, tlev))


def _test_wavelet(img, wav, tval, tlev, tmode):
    """Calculates all the metrics on a given wavelet"""
    img_dat = read_image(img, _args.grayscale)
    dwt_dat = dwt(img_dat, wav, dl=tlev)
    den_dat = threshold(dwt_dat, tval, mode=tmode)
    den_img = idwt(den_dat, wav)
    img_no_a = remove_alpha(den_img)
    n_f = save_image(img, img_no_a)
    _cr = calc_compression(img, n_f)
    _pr = pearson(img_dat, img_no_a)
    _r = calc_nrmse(img_dat.ravel(), img_no_a.ravel())
    return _pr, _r, _cr


def read_image(file, is_gray=False):
    """Reads an image with opencv"""
    if _args.verbose:
        print('Reading image <{}>...'.format(file), end='')
    if is_gray:
        d = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    else:
        d = cv2.imread(file)
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


def idwt(data, wav):
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


def remove_alpha(data):
    """
    Check if we should remove the alpha channel

    Use with caution, as it ignores transparency on images!
    """
    if not _args.grayscale:
        data = data[:, :, :3].astype('uint8')
    return data


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
    threshold_value = int(args.threshold)
    threshold_mode = args.mode
    dec_level = int(args.levels)

    if not os.path.isfile(args.image):
        print('Given file <{}> does not exist!'.format(args.image))
        sys.exit(1)

    if args.wavelets:
        print('Available wavelets:')
        print(pywt.wavelist(kind='discrete'))

    image_file = args.image
    if args.wavelet == 'test':
        # Test some discrete wavelets in pywt
        wavelets = ['bior1.1', 'bior1.3', 'rbio1.1', 'haar', 'db1', 'db4', 'coif1', 'sym2']
        test_wavelets(image_file, threshold_value, dec_level, threshold_mode, wavelets)
    else:
        wavelet = pywt.Wavelet(args.wavelet)
        # Preberi sliko s pomocjo opencv
        image_data = read_image(image_file, args.grayscale)

        # Na sliki izvedi DWT (diskretna valcna transformacija)
        dwt_data = dwt(image_data, wavelet, dl=dec_level)
        # Izvedi mehko ali trdo pragovno funkcijo
        denoised_data = threshold(dwt_data, threshold_value, mode=threshold_mode)

        # Rekonstruiraj sliko
        denoised_image = idwt(denoised_data, wavelet)
        # V primeru png odstrani morebitni alpha kanal (problem ce delas z 24bit RGB slikami,
        # opencv doda alpha kanal in slika postane 32bit RGBA)
        # V kolikor je grayscale ali png se ne zgodi nic
        image_no_alpha = remove_alpha(denoised_image)

        # Pearson korelacija
        pr = pearson(image_data, image_no_alpha)

        # normaliziran RMSE
        r = calc_nrmse(image_data.ravel(), image_no_alpha.ravel())

        # Shrani sliko v _new
        new_file = save_image(image_file, image_no_alpha)

        # Izracunaj razmerje stiskanja
        cr = calc_compression(image_file, new_file)

        # Prikazi rezultate
        print_metrics(pr, r, cr, new_file, threshold_value, threshold_mode, dec_level, wavelet)


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('image', help='path to an image (jpg or png)')
    _parser.add_argument('wavelet', help='wavelet name, e.g. "haar" or "db1", set to "all" to test for best')
    _parser.add_argument('-g', '--grayscale', help='set when using a grayscale image', action='store_true')
    _parser.add_argument('-w', '--wavelets', help='list wavelets available', action='store_true')
    _parser.add_argument('-v', '--verbose', help='output more info about current operations', action='store_true')
    _parser.add_argument('-t', '--threshold', help='threshold value')
    _parser.add_argument('-m', '--mode', help='threshold mode')
    _parser.add_argument('-l', '--levels', help='decomposition levels')
    params = _parser.parse_args()

    main(params)
