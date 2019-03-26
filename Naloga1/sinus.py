#!/usr/bin/env python3
#
# Program za izris poljubne sinusoide, pri cemer lahko
# nastavimo parametre amplitude, frekvence, faze in tudi
# vzorcevalne frekvence.
#
# Pri izdelavi sem za navdih uporabil
# http://195.134.76.37/applets/AppletNyquist/Appl_Nyquist2.html
#
# author    David Rubin
# url       https://github.com/rubinda/rosis/naloga1
import sys
import math
import numpy
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Sinusoide'
        self.amp_input = QLineEdit()
        self.phase_input = QLineEdit()
        self.freq_input = QLineEdit()
        self.samp_freq_input = QLineEdit()
        self.time_limit = QLineEdit()
        self.draw_button = QPushButton('Narisi', self)
        self.type_group = QButtonGroup();
        self.normal_sin = QRadioButton("Navadna")
        self.analy_sin = QRadioButton("Analiticna")
        self.type_group.addButton(self.normal_sin, 1)
        self.type_group.addButton(self.analy_sin, 2)

        self.initUI()

    def initUI(self):
        layout = QFormLayout()
        # Vhod za amplitudo
        self.amp_input.setText('1')
        layout.addRow('Amplituda', self.amp_input)

        # Vhod za fazo
        self.phase_input.setText('0')
        layout.addRow('Faza', self.phase_input)

        # Vhod za frekvenco
        self.freq_input.setText('10')
        layout.addRow('Frekvenca', self.freq_input)

        # Vhod za vzorcevalno frekvenco
        self.samp_freq_input.setText('20')
        layout.addRow('Vzor. frek.', self.samp_freq_input)

        # Vhod za casovni interval
        self.time_limit.setText('0.2')
        layout.addRow('Casovni interval', self.time_limit)

        # Grupa za analiticno ali navadno sinusoido
        self.analy_sin.setChecked(True)
        layout.addRow("Vrsta funkcije", self.analy_sin)
        layout.addRow(" ", self.normal_sin)

        # Gumb za izris grafa
        self.draw_button.setToolTip('Izrisi sinusoido s podanimi parametri')
        self.draw_button.clicked.connect(self.handle_graph_button)
        layout.addRow(self.draw_button)

        self.setLayout(layout)
        self.show()

    def handle_graph_button(self):
        amp = float(self.amp_input.text())
        pha = float(self.phase_input.text())
        fre = float(self.freq_input.text())
        sfr = float(self.samp_freq_input.text())
        tim = float(self.time_limit.text())
        typ = int(self.type_group.checkedId())

        make_graph(amplitude=amp, phase=pha, frequency=fre, sampling_rate=sfr, time_limit=tim, graph_type=typ)


def make_graph(amplitude=1.0, phase=0.0, frequency=1.0, sampling_rate=100.0, time_limit=2.0, graph_type=1):
    """
    Narise graf sinusoide s podanimi parametri

    :param amplitude: amplituda
    :param phase: faza (odmik)
    :param frequency: frekvenca v Hz
    :param sampling_rate: vzorcevalna frekvenca v Hz
    :param time_limit: zgornja meja casovnega
    :param graph_type: tip grafa (1 => navadna sinusoida, 2=> analiticna)
    :return: None
    """
    # Casovni interval, ki ga doloci GUI
    time_interval = numpy.arange(0, time_limit, 1/sampling_rate)
    # Standardni casovni interval (10k tock) za lepsi izris ("Dejanski" signal
    proper_time = numpy.arange(0, time_limit, 1/10000)

    fig = plt.figure(figsize=(13, 8))

    # Preveri ali risemo navadno (1) ali analiticno funkcijo (2)
    if graph_type == 2:
        # Uporabimo Eulerjevo formulo za izracun tock
        # A*e^(j * 2pi * f * t + faz) = Asin(2pi *f *t +faz) + j*A*cos(2pi *f *t +faz)
        result = amplitude * numpy.sin(time_interval * 2 * math.pi * frequency + phase) \
            + 1j * amplitude * numpy.cos(time_interval * 2 * math.pi * frequency + phase)

        # Za izris "dejanskega" signala uporabimo vec tock
        proper_result = amplitude * numpy.sin(proper_time * 2 * math.pi * frequency + phase) \
                        + 1j * amplitude * numpy.cos(proper_time * 2 * math.pi * frequency + phase)

        # Povej matplotlib da risemo 3D
        ax = fig.gca(projection='3d')

        # Narisi tocke kot scatter in plotaj "dejansko" krivuljo kot line
        ax.scatter(time_interval, result.real, result.imag, label='Vzorcne tocke', color='red')
        ax.plot(proper_time, proper_result.real, proper_result.imag, label='"Dejanski" signal', alpha=0.5)

    else:
        # Poracunaj tocke za realno sinusoido
        result = amplitude * numpy.sin(time_interval * 2 * math.pi * frequency + phase)
        ax = fig.gca()

        # V kolikor ne vzorcimo z vsaj 2*frequency narisi se alias frekvenco
        if sampling_rate / frequency < 2:
            alias_frequency = frequency - 1 * sampling_rate
            ax.plot(proper_time, amplitude * numpy.sin(proper_time * 2 * math.pi * alias_frequency + phase),
                    linestyle='dashed', color='green', label='Alias frekvenca')

        # Izrisi "dejanski" signal in vzorcne tocke
        ax.plot(proper_time, amplitude * numpy.sin(proper_time * 2 * math.pi * frequency + phase),
                label='"Dejanski" signal', alpha=0.5)
        ax.scatter(time_interval, result, label='Vzorcne tocke', color='red')

    # Prestavi legendo desno zraven grafa, in nastavi nekaj parametrov za lepsi prikaz
    ax.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    plt.title(str(frequency) + 'Hz sinusoida vzorcena z ' + str(sampling_rate) + 'Hz')
    plt.xlabel('Čas [s]')
    plt.locator_params(nbins=5)
    plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
