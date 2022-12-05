# -*- coding: utf-8 -*-

import sys
from PyQt6 import QtGui, QtWidgets

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

from Functions import Sinusoid


# Кастомный канвас для виджета отображения графиков (наследник канваса мпл)
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Получаем фигуру для размещения графиков и оси
        self.fig, self.ax = plt.subplots()
        # Делаем полотно сетчатым
        self.ax.grid()
        # Устанавливаем лимиты отображения нашей плоскости
        plt.xlim([-10.6, 10.6])
        plt.ylim([-3.2, 3.2])

        # Вызываем констрктор класса предка, чтобы он выполнил все необходимые методы matplotlib
        FigureCanvas.__init__(self, self.fig)
        # "Втыкаем" полотно в объект, пришедший из конструктора
        self.setParent(parent)


# Виджет для отображения анимированных графиков на полотне
class AnimationWidget(QtWidgets.QWidget):
    def __init__(self):
        # Вызываем констрктор класса предка, чтобы он выполнил все необходимые методы PyQt6
        QtWidgets.QWidget.__init__(self)

        # Верстаем интерфейс виджета, он состоит из 2 блоков - vbox и hbox
        # vbox содержит наше полотно, класс которого описан выше
        vbox = QtWidgets.QVBoxLayout()
        self.canvas = MyMplCanvas(self)
        vbox.addWidget(self.canvas)

        # hbox - содержит лишь кнопки, что видны под нашим полотном
        hbox = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Старт", self)
        self.stop_button = QtWidgets.QPushButton("Пауза", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.stop_button.setFont(font)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)

        # Окончательно собираем интерфейс
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # При запуске программы полотно изначально стоит на паузе
        self.isPaused = True

        # Массив отображаемых на полотне объектов
        self.objects = []
        # Массив анимаций (FuncAnimation) задаваемых нашими объектами
        self.animations = []
        # При инициализации виджета создаем один отображаемый объект и сразу удаляем его линию
        # Костыль конечно, но иначе не хочет работать (вернее добавлять новые объекты динамически)
        self.add_object(1)
        self.objects[0].line.remove()

    # Данная функция выполняется при нажатии на кнопку "Старт"
    # Переводит атрибут текущего класса и каждого объекта из self.objects isPaused в значение False
    # Возобновляет воспроизведение анимации
    def on_start(self):
        self.isPaused = False
        for item in self.objects:
            item.isPaused = False

    # Данная функция выполняется при нажатии на кнопку "Пауза"
    # Переводит атрибут текущего класса и каждого объекта из self.objects isPaused в значение True
    # Приостанавливает воспроизведение анимации
    def on_stop(self):
        self.isPaused = True
        for item in self.objects:
            item.isPaused = True

    # Данный метод вызывается при создании новых объектов анимации из main.py
    # Создает новый объект и добавляет необходимые значения в self.objects и self.animations
    def add_object(self, params):
        s = Sinusoid(plt, self.canvas.ax, params)
        gen = s.data_gen()
        anim = FuncAnimation(self.canvas.figure, s.update, gen, interval=20, blit=False)
        s.isPaused = self.isPaused
        self.objects.append(s)
        self.animations.append(anim)


# Реликт для проверки работы виджета
if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec())
