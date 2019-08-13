#!/usr/bin/env python3
#
# Beat Detection algorithm, based on the article:
# Musical Genre Classification of Audio Signals
# George Tzanetakis, Student Member, IEEE, and Perry Cook, Member, IEEE
#
# Regarding the report (porocilo.pdf):
#   The baseline BPM for a given song is taken from https://www.cs.ubc.ca/~davet/music/bpm/index.html
#
# @author David Rubin, 2019
import pywt
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import scipy.signal


def rescale(arr, factor=2):
    """Rescales the given array with the given factor (currently not used)"""
    n = len(arr)
    return np.interp(np.linspace(0, n, factor*n), np.arange(n), arr)


def plt_signal(sig, time, fignum, title, xlabel="", ylabel=""):
    """Plots the given data (!) does not call plt.show()"""
    plt.figure(fignum)
    plt.plot(time, sig)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def single_peak(sig):
    """Returns the index of the single highest peak in the signal
    (if multiple are present with the same value return the first one)"""
    max_idx = np.where(sig == np.amax(sig))
    if len(max_idx[0]) > 1:
        # More than one value are maximums, return the first one
        return max_idx[0][0]
    return max_idx[0]


def n_peaks(sig, n=3):
    """Return the n (default=3) highest (value) peak indices"""
    return sig.argsort()[::-1][:n]


def autocorrelate(x):
    """Autocorrelate the given signal using numpy"""
    result = np.correlate(x, x, mode='full')
    return result[len(result) // 2:]


def envelope(signal, subs=16):
    """A simple signal envelope"""
    # Absolute signal value
    z = np.absolute(signal)
    # Smoothing (filtering)
    w = scipy.signal.lfilter([0.01], [0.99], z)
    # Subsample
    w = w[::subs]
    # Subtract the average
    avg = np.mean(w)
    return w - avg


def get_bpm(data, fs, lvls=4, max_dec=16, pks=1, aprx='median'):
    """Calculates the approximate BPM for the given data"""

    # DWT with 'db4' and n decomposition levels
    song_dwt = pywt.wavedec(data, wavelet='db4', level=lvls)
    # Prvi izhod je aproksimacija na podani stopnji, ostalo so detajli
    cdminlen = int(len(song_dwt[4]) / max_dec + 1)
    song_approx = np.zeros(cdminlen)

    # Calculate the envelope and decimate for the correct ammount (the levels are
    # given the in reverse order (lvl 0/1 = max level of DWT)
    for lvl, band in enumerate(song_dwt):
        sub_factor = lvl - 1 if lvl-1 > 0 else 0
        env = envelope(band, subs=2**sub_factor)
        song_approx = env[:cdminlen] + song_approx
    # plt_signal(song_approx, time=np.linspace(0, len(song_approx)/step, num=len(song_approx)),
    #           fignum=2, title='Aproksimacija na nivoju {}'.format(levels))
    
    # Get the min and max index for the appropriate interval on the data
    # (between 40 and 220 BPMs)
    min_idx = int(60. / 220 * (fs / max_dec))
    max_idx = int(60. / 40 * (fs / max_dec))
    corr = autocorrelate(song_approx)

    # Use a single peak or multiple
    if pks < 2:
        peak_idx = single_peak(corr[min_idx:max_idx])
        peak_bpm = int(60. / (peak_idx + min_idx) * fs / max_dec)
        return peak_bpm
    else:
        # Find the peaks on the given interval and select the N (=pks) most prominent ones
        peaks = scipy.signal.find_peaks(corr[min_idx:max_idx], distance=5)[0]
        prominences = scipy.signal.peak_prominences(corr[min_idx:max_idx], peaks, wlen=5)[0]
        prominent_peaks = sorted(zip(peaks, prominences), key=lambda p: p[1], reverse=True)[:pks]
        if len(prominent_peaks) < 1:
            # No peaks are present in the signal, BPM is 0?
            return 0
        else:
            win_bpms = []
            # Convert the peaks to BPM
            for peak, prominence in prominent_peaks:
                # peak_amp = corr[peak + min_idx]
                win_bpms.append(60. / (peak + min_idx) * fs / max_dec)
            if aprx == 'median':
                current_bpm = np.median(win_bpms)
            elif aprx == 'mean':
                current_bpm = np.mean(win_bpms)
            else:
                raise ValueError('Approximation method "{}" not recognized'.format(aprx))
            return current_bpm


def main(file_name, levels=4, window_duration=5, peak_count=1, approx='mean', silent=False):
    """
    Run BPM detection on a file. The window is shifted for 1 second (e.g. win_duration=5: 0-5, 1-6, 2-7, 3-8 ...).

    :param file_name: the song in .wav format
    :param levels: DWT decomposition levels
    :param window_duration: Duration of the window for which BPM is calculated
    :param silent: when set True it does not draw a graph or print out the result
    :param peak_count: number of autocorrelation peaks to take into account
    :param approx: approximation method (mean or median)
    :return: average BPM for the file and each window
    """
    max_decimation = 2 ** levels    # maximum subsample of original data from DWT
    sample_pointer = 0  # current sample position
    fs, song = wavfile.read(file_name)
    window_samples = window_duration * fs   # samples in a window
    window_count = len(song)//fs - window_duration  # number of windows we will process
    window_bpm = np.zeros(window_count)     # bpm for each window
    bpm_sample = np.zeros(window_count)     # pointer for the first sample of each window

    # keep only 1 channel (stereo to mono)
    song_mono = song[:, 0]
    for win_idx in range(0, window_count):
        # Extract the next window from song data
        data = song_mono[sample_pointer:sample_pointer + window_samples]

        # Calculate and store the average BPM for the given window
        win_bpm = get_bpm(data, fs, lvls=levels, max_dec=max_decimation, pks=peak_count, aprx=approx)
        window_bpm[win_idx] = win_bpm
        bpm_sample[win_idx] = sample_pointer

        # Move to the next window (0..N, 1..N+1, 2..N+2 ...)
        sample_pointer += fs    # move to the next second

    # Calculate the average (median) BPM for the whole file
    if approx == 'median':
        approx_bpm = np.median(window_bpm)
    elif approx == 'mean':
        approx_bpm = np.mean(window_bpm)
    else:
        raise ValueError('Approximation method "{}" not recognized'.format(approx))

    if not silent:
        # Plot the bpm through time
        plt.plot(bpm_sample/fs, window_bpm)
        plt.title('{} BPM={:.2f}'.format(file_name, approx_bpm))
        plt.xlabel('Time [seconds]')
        plt.ylabel('BPM [beats/min]')
        plt.show()
        print('Done:\n Song:\t{}\n BPM:\t{:.2f}'.format(file_name, approx_bpm))
    return approx_bpm, window_bpm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate BPM of a song using DWT.')
    parser.add_argument('file', help='A file (song) in .wav format')
    parser.add_argument('-l', '--levels', help='DWT decomposition levels', default=4)
    parser.add_argument('-w', '--window', help='Duration of the window in seconds (BPM calculated for each)',
                        default=5, type=int)
    parser.add_argument('-p', '--peaks', help='How many (autocorrelation) peaks to use for BPM calculation',
                        default=1, type=int)
    parser.add_argument('-a', '--approx', help='Approximation method', choices=['mean', 'median'], default='median')
    args = parser.parse_args()
    main(args.file, args.levels, args.window, args.peaks, args.approx)
