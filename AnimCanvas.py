# -*- coding: utf-8 -*-

import sys
from PyQt6 import QtGui, QtWidgets

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

from Functions import *


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
        self.gif_button = QtWidgets.QPushButton("Сохранить", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.gif_button.clicked.connect(self.on_save)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.stop_button.setFont(font)
        self.gif_button.setFont(font)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.gif_button)

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

        # victim = Victim(plt, self.canvas.ax, start_x=0, start_y=0, direction=30, speed=0.3, max_angle_of_rotation=45,
        #                 angle_of_vision=30, len_of_vision=10)
        # hunter =Hunter(plt, self.canvas.ax, start_x=-4, start_y=2, direction=-10, speed=0.5, max_angle_of_rotation=10,
        #                  angle_of_vision=30, len_of_vision=10)
        #
        # victim.add_hunter(hunter1)
        # hunter1.set_victim(victim)
        #
        # self.objects.append(victim)
        # self.objects.append(hunter1)
        #
        # gen1 = victim.data_gen()
        # self.animations.append(FuncAnimation(self.canvas.figure, victim.update, gen1, interval=20, blit=False))
        # gen2 = hunter1.data_gen()
        # self.animations.append(FuncAnimation(self.canvas.figure, hunter1.update, gen2, interval=20, blit=False))

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

    def on_save(self):
        print('aboba')

    # Данный метод вызывается при создании новых объектов анимации из main.py
    # Создает новый объект и добавляет необходимые значения в self.objects и self.animations
    def add_object(self, plane_type, v_start_x=0, v_start_y=0, v_direction=0, v_speed=0.5,
                   v_max_angle_of_rotation=10,
                   v_angle_of_vision=0, v_len_of_vision=0):

        if plane_type == 'victim':
            obj = Victim(plt, self.canvas.ax, start_x=v_start_x, start_y=v_start_y, direction=v_direction,
                         speed=v_speed,
                         max_angle_of_rotation=v_max_angle_of_rotation,
                         angle_of_vision=v_angle_of_vision, len_of_vision=v_len_of_vision)
        elif plane_type == 'hunter':
            obj = Hunter(plt, self.canvas.ax, start_x=v_start_x, start_y=v_start_y, direction=v_direction,
                         speed=v_speed,
                         max_angle_of_rotation=v_max_angle_of_rotation,
                         angle_of_vision=v_angle_of_vision, len_of_vision=v_len_of_vision)
        else:
            obj = Sinusoid(plt, self.canvas.ax, 1)

        gen = obj.data_gen()
        anim = FuncAnimation(self.canvas.figure, obj.update, gen, interval=20, blit=False)
        obj.isPaused = self.isPaused
        self.objects.append(obj)
        self.animations.append(anim)

        return obj


# Реликт для проверки работы виджета
if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec())
