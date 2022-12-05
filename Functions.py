import numpy as np
from collections import deque


class Sinusoid(object):
    def __init__(self, plt, ax, k=1.0, n_points=500):
        self.n_points = n_points
        self.e = 10 / n_points
        self.k = k
        npx = np.linspace(0, 0, 1)
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(np.sin(self.k * np.pi * npx), maxlen=n_points)
        self.x_history = [self.x[0]]
        self.y_history = [self.y[0]]
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.color = None
        # self.plt.xlim([-10.6, 10.6])
        # self.plt.ylim([-5.2, 5.2])

    def update(self, dy):
        last = self.x[-1]
        if not self.isPaused:
            self.x.append(last + self.e)  # update data
            self.y.append(dy)
            self.x_history.append(last + self.e)
            self.y_history.append(dy)

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)

            # лимиты осей (с какой по какую точку оси отображать плот)
            if last < 10:
                self.plt.xlim([-0.6, 10.6])
            else:
                self.plt.xlim([last - 10.6, last + 0.6])
            self.plt.ylim([-1.2, 1.2])
            self.ax.autoscale_view(True, True, True)

            return self.line, self.ax

    def data_gen(self):
        while True:
            yield np.sin(self.k * np.pi * self.x[-1])

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)

