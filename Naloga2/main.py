import sys
import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.Title = 'Sestevanje sinusoid'

        # Sinusoida 1
        self.input_frequency1 = QLineEdit('1')
        self.input_phase1 = QLineEdit('1')
        self.input_amplitude1 = QLineEdit('1')

        # Sinusoida 2
        self.input_amplitude2 = QLineEdit('2')
        self.input_frequency2 = QLineEdit('2')
        self.input_phase2 = QLineEdit('2')

        # Sinusoida 3
        self.input_amplitude3 = QLineEdit('3')
        self.input_frequency3 = QLineEdit('3')
        self.input_phase3 = QLineEdit('3')

        # Sinusoida 4
        self.input_amplitude4 = QLineEdit('4')
        self.input_frequency4 = QLineEdit('4')
        self.input_phase4 = QLineEdit('4')

        # Vzorcenje
        self.input_sampling_rate = QSpinBox()
        self.input_sampling_rate.setMaximum(10000)
        self.input_sampling_rate.setMinimum(1)
        self.input_sampling_rate.setValue(100)
        self.InitUI()

    def InitUI(self):
        layout_main = QVBoxLayout()

        layout_sin1_form = QFormLayout()
        layout_sin1_form.addRow('Amplituda', self.input_amplitude1)
        layout_sin1_form.addRow('Frekvenca', self.input_frequency1)
        layout_sin1_form.addRow('Faza', self.input_phase1)

        layout_sin1 = QVBoxLayout()
        layout_sin1.addWidget(QLabel("Sinusoida 1"))
        layout_sin1.addLayout(layout_sin1_form)
        layout_main.addLayout(layout_sin1)

        layout_sin2_form = QFormLayout()
        layout_sin2_form.addRow('Amplituda', self.input_amplitude2)
        layout_sin2_form.addRow('Frekvenca', self.input_frequency2)
        layout_sin2_form.addRow('Faza', self.input_phase2)

        layout_sin2 = QVBoxLayout()
        layout_sin2.addWidget(QLabel("Sinusoida 2"))
        layout_sin2.addLayout(layout_sin2_form)
        layout_main.addLayout(layout_sin2)

        layout_sin3_form = QFormLayout()
        layout_sin3_form.addRow('Amplituda', self.input_amplitude3)
        layout_sin3_form.addRow('Frekvenca', self.input_frequency3)
        layout_sin3_form.addRow('Faza', self.input_phase3)

        layout_sin3 = QVBoxLayout()
        layout_sin3.addWidget(QLabel("Sinusoida 3"))
        layout_sin3.addLayout(layout_sin3_form)
        layout_main.addLayout(layout_sin3)

        layout_sin4_form = QFormLayout()
        layout_sin4_form.addRow('Amplituda', self.input_amplitude4)
        layout_sin4_form.addRow('Frekvenca', self.input_frequency4)
        layout_sin4_form.addRow('Faza', self.input_phase4)

        layout_sin4 = QVBoxLayout()
        layout_sin4.addWidget(QLabel("Sinusoida 4"))
        layout_sin4.addLayout(layout_sin4_form)
        layout_main.addLayout(layout_sin4)

        layout_main.addLayout(layout_sin1)

        self.setLayout(layout_main)

        layout_sin4_form.addRow("F. vzorcenja", self.input_sampling_rate)

        canvas = FigureCanvas(Figure(figsize=(6, 6), dpi=100))
        layout_main.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self._timer = canvas.new_timer(interval=20)
        self._timer.add_callback(self.update_canvas)
        self._timer.start()


    def update_canvas(self):
        time_interval = np.arange(0, 3, 1/self.input_sampling_rate.value())
        A1 = float(self.input_amplitude1.text() or 0)
        A2 = float(self.input_amplitude2.text() or 0)
        A3 = float(self.input_amplitude3.text() or 0)
        A4 = float(self.input_amplitude4.text() or 0)
        f1 = float(self.input_frequency1.text() or 0)
        f2 = float(self.input_frequency2.text() or 0)
        f3 = float(self.input_frequency3.text() or 0)
        f4 = float(self.input_frequency4.text() or 0)
        p1 = float(self.input_phase1.text() or 0)
        p2 = float(self.input_phase2.text() or 0)
        p3 = float(self.input_phase3.text() or 0)
        p4 = float(self.input_phase4.text() or 0)

        s1 = A1 * np.sin(2 * np.pi * f1 * (time_interval + time.time()) + p1)
        s2 = A2 * np.sin(2 * np.pi * f2 * (time_interval + time.time()) + p2)
        s3 = A3 * np.sin(2 * np.pi * f3 * (time_interval+ time.time()) + p3 )
        s4 = A4 * np.sin(2 * np.pi * f4 * (time_interval+ time.time()) + p4 )

        self.ax.clear()
        self.ax.set_xlim([0, 3.2])
        self.ax.plot(time_interval, s1+s2+s3+s4)
        self.ax.figure.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
