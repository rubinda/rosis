import numpy as np
import matplotlib; matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import animation

# casovni interval
time_interval = np.arange(0, 5, 0.01)
fig, ax = plt.subplots()
ax.set_ylim([-10, 10])
ax.set_xlim([0, 5.5])
line, = ax.plot(time_interval, np.sin(time_interval))


def main():
    line_ani = animation.FuncAnimation(fig, animate, np.arange(1, 10000), interval=25, blit=True)
    plt.show()


def animate(i):
    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4
    f1 = 10
    f2 = 2
    f3 = 7
    f4 = 4
    s1 = np.sin(A1 * np.pi * f1 * time_interval + i/10 + 1)
    s2 = np.sin(A2 * np.pi * f2 * time_interval + i/10 + 2)
    s3 = np.sin(A3 * np.pi * f3 * time_interval + i/10 + 3)
    s4 = np.sin(A4 * np.pi * f4 * time_interval + i/10 + 4)
    line.set_ydata(s1 + s2 + s3)
    return line,


if __name__ == '__main__':
    main()
