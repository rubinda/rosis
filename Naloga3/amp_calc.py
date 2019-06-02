#!/usr/bin/env python3
#
# Skripta, ki oceni odvisnost amplitude glede na razdaljo od zvoka
#
# @author David Rubin
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert


def readWAV(filename):
    """ Prebere datoteko in vrne podatke o amplitudah"""
    fs, data = wavfile.read(filename)
    return fs, data


def amplitude(signal):
    """ Returns the amplitude of the given signal"""
    #fft_signal = np.fft.fft(signal, n=262144)
    fft_signal = hilbert(signal, N=262144)
    amplitude = np.abs(fft_signal)
    return amplitude


fs, d = readWAV('zvizgi/zvizg5.wav')
spectre = np.fft.fft(d)
freq = np.fft.fftfreq(d.size//2, 1/fs)
mask = freq > 0
plt.plot(freq[mask], np.abs(spectre[mask]))
plt.show()


'''amps_left = amplitude(d[:, 0])
print(amps_left)
amps_right = amplitude(d[:, 1])
plt.subplot(2, 1, 1)
plt.plot(amps_left)
plt.ylabel("Amplitude levega kanala")

plt.subplot(2, 1, 2)
plt.plot(amps_right)
plt.ylabel("Amplitude desnega kanala")
plt.show()
'''
