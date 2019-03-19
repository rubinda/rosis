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
        self.freq_input.setText('1')
        layout.addRow('Frekvenca', self.freq_input)

        # Vhod za vzorcevalno frekvenco
        self.samp_freq_input.setText('100')
        layout.addRow('Vzor. frek.', self.samp_freq_input)

        # Vhod za casovni interval
        self.time_limit.setText('10')
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

        make_graph(amp, pha, fre, sfr, tim, typ)


def make_graph(amplitude=1, phase=1, frequency=1, sampling_rate=100, time_limit=10, type=1):
    """
    Narise graf sinusoide s podanimi parametri

    :param amplitude: amplituda
    :param phase: faza (odmik)
    :param frequency: frekvenca v Hz
    :param sampling_rate: vzorcevalna frekvenca v Hz
    :param time_limit: zgornja meja casovnega
    :param type: tip grafa (1 => navadna sinusoida, 2=> analiticna)
    :return: None
    """
    time_interval = numpy.arange(0, time_limit, 1/sampling_rate)

    fig = plt.figure()

    # Preveri ali risemo navadno (1) ali analiticno funkcijo (2)
    if type == 2:
        # Uporabimo Eulerjevo formulo za izracun tock
        # A*e^(j * 2pi * f * t + faz) = Asin(2pi *f *t +faz) + j*A*cos(2pi *f *t +faz)
        result = amplitude * numpy.sin(time_interval * 2 * math.pi * frequency + phase) \
            + 1j * amplitude * numpy.cos(time_interval * 2 * math.pi * frequency + phase)
        ax = fig.gca(projection='3d')
        ax.plot(time_interval, result.real, result.imag)
        plt.show()
    else:
        result = amplitude * numpy.sin(time_interval * 2 * math.pi * frequency + phase)
        fig, ax = plt.subplots()
        ax.plot(time_interval, result)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
