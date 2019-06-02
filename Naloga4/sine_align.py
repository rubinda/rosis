#!/usr/bin/env python3
#
# Program, ki omogoca natanco poravnavo dveh sinusoid
#
# @author David Rubin
import numpy as np
from scipy.io import wavfile


def shift_mono_to_stereo(filename, distance):
    """
    Premakne mono zvocno datoteko za dolocen cas (simulira stereo zajem)
    @:parameter filename datoteka ki vsebuje mono zvok
    @:parameter distance razdalja med mikrofonoma, ki jo simuliramo (v metrih)
    """
    v_sound = 343  # m/s
    fs, mono = wavfile.read(filename)

    # Ustvari stereo array in en kanal napolni z mono
    signal = np.zeros((len(mono), 2), dtype=np.int16)
    signal[:, 0] = mono

    # Zamakni signal za N vzorcev (pridobi iz razdalje med mikrofonoma in hitrostjo
    # Predvidevamo, da sta mikrofona v premici z izvorom zvoka
    shifted = np.copy(mono)
    delay = distance / v_sound
    samples = round(fs * delay)
    shifted = np.roll(shifted, samples)
    signal[:, 1] = shifted
    # print('Shifting the sound for {}s ({} samples)'.format(delay, samples))

    wavfile.write('stereo.wav', fs, signal)


def read_stereo(filename):
    """ Prebere stereo datoteko in vrne sampling rate, levi in desni kanal v seznamih """
    fs, stereo = wavfile.read(filename)
    return fs, stereo[:, 0], stereo[:, 1]


fs, left, right = read_stereo('stereo.wav')
dftL = np.fft.fft(left)
phaseL = np.angle(dftL)

print(phaseL)