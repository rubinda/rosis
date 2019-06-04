#!/usr/bin/env python3
#
# Izgradi nestabilen fileter in ga popravi v stabilnega
#
# @author David Rubin
import numpy as np
import matplotlib.pyplot as plt
from zplane import zplane
from scipy import signal


b = np.array([2, 1, -1/9, 0, 1, -7/11, 2])  # b koeficienti filtra (nicle)
a = np.array([3/4, -1, 2/3, -6/13, -25/29, -3, 3/8])  # a koeficient filtra (poli)


def plot_freq_response(h, w, filename, fignum=2):
    """ Shrani png frekvencnega odziva v datoteko"""
    plt.figure(fignum)
    plt.plot(w, 20 * np.log10(abs(h)), label='Frekvenčni odziv')
    plt.xlabel('Normalizirana frekvenca [x pi rad/sample]')
    plt.ylabel('Amplituda [dB]')
    plt.savefig(filename)


def plot_impulse_response(t, y, filename, fignum=3):
    """" Shrani png impulznega odziva v datoteko """
    plt.figure(fignum)
    plt.plot(t, y, label='Impulzni odziv')
    plt.xlabel('Številka vzorca')
    plt.ylabel('Amplituda')
    plt.savefig(filename)


# Izrise graf, v kolikor podano se 3 argument shrani sliko v datoteko
zeros, poles, _ = zplane(b, a, 'images/zplane_before.png')

# Poracunaj frekvencni odziv filtra
# Vraca
# w ... The normalized frequencies at which h was computed, in radians/sample.
# h ... The frequency response
w, h = signal.freqz(b, a)
w = w/np.pi
plot_freq_response(h, w, 'images/freq-response_before.png', fignum=2)

# Poracunaj impulzni odziv filtra
t, y = signal.impulse((b, a))
plot_impulse_response(t, y, 'images/impulse-response_before.png', fignum=3)


# Stabiliziraj filter ( ~p = 1/p* ... p* complex conjugation)
# https://dsp.stackexchange.com/questions/26114/how-to-stabilize-a-filter
new_poles = np.array(poles, copy=True)
for i, pole in enumerate(poles):
    if np.abs(pole) > 1:
        new_poles[i] = 1 / np.conj(pole)

fix_a = np.poly(new_poles)
print(fix_a)
zplane(b, fix_a, 'images/zplane_after.png', fignum=4)

# Poracunaj frekvencni odziv popravljenega filtra
w, h = signal.freqz(b, fix_a)
w = w/np.pi
plot_freq_response(h, w, 'images/freq-response_after.png', fignum=5)

# Poracunaj impulzni odziv popravljenega filtra
t, y = signal.impulse((b, fix_a))
plot_impulse_response(t, y, 'images/impulse-response_after.png', fignum=6)