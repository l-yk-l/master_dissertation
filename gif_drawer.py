import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import math
import numpy as np


__N = 0
__flag = True


def __get_filename():
    filename = datetime.now()
    filename = str(filename).split('.')[0]
    filename = filename.replace(' ', '_')
    filename = filename.replace(':', '-')
    filename += '.gif'
    return filename


def __draw_vision(obj, left_border, right_border, n):
    # Расчет координат точек конуса обзора
    if obj.type == 'victim':
        obj.vision_left_border_x = obj.x_history[n] + obj.len_of_vision * np.cos(
            np.radians(180+obj.direction - (obj.angle_of_vision / 2)))
        obj.vision_left_border_y = obj.y_history[n] + obj.len_of_vision * np.sin(
            np.radians(180+obj.direction - (obj.angle_of_vision / 2)))
        obj.vision_right_border_x = obj.x_history[n] + obj.len_of_vision * np.cos(
            np.radians(180+obj.direction + (obj.angle_of_vision / 2)))
        obj.vision_right_border_y = obj.y_history[n] + obj.len_of_vision * np.sin(
            np.radians(180+obj.direction + (obj.angle_of_vision / 2)))

    elif obj.type == 'hunter':
        obj.vision_left_border_x = obj.x_history[n] + obj.len_of_vision * np.cos(
            np.radians(obj.direction - (obj.angle_of_vision / 2)))
        obj.vision_left_border_y = obj.y_history[n] + obj.len_of_vision * np.sin(
            np.radians(obj.direction - (obj.angle_of_vision / 2)))
        obj.vision_right_border_x = obj.x_history[n] + obj.len_of_vision * np.cos(
            np.radians(obj.direction + (obj.angle_of_vision / 2)))
        obj.vision_right_border_y = obj.y_history[n] + obj.len_of_vision * np.sin(
            np.radians(obj.direction + (obj.angle_of_vision / 2)))

    left_border.set_xdata(np.linspace(obj.x_history[n], obj.vision_left_border_x, math.ceil(obj.len_of_vision) * 6))
    left_border.set_ydata(np.linspace(obj.y_history[n], obj.vision_left_border_y, math.ceil(obj.len_of_vision) * 6))
    right_border.set_xdata(np.linspace(obj.x_history[n], obj.vision_right_border_x, math.ceil(obj.len_of_vision) * 6))
    right_border.set_ydata(np.linspace(obj.y_history[n], obj.vision_right_border_y, math.ceil(obj.len_of_vision) * 6))


def __update(n, x, y, line, left_border, right_border, obj):
    global __flag
    if n == __N-1:
        __flag = False
    if __flag:
        line.set_xdata(x[:n+1])
        line.set_ydata(y[:n+1])
        print(1111)
        __draw_vision(obj, left_border, right_border, n)


def __update_all(n, *args):
    print('qq')
    min_x_lim = min(args[0][:n+1])
    min_y_lim = min(args[1][:n+1])
    max_x_lim = max(args[0][:n+1])
    max_y_lim = max(args[1][:n+1])
    for i in range(6, len(args), 6):
        min_x_lim = min(min_x_lim, min(args[i][:n+1]))
        min_y_lim = min(min_y_lim, min(args[i+1][:n+1]))
        max_x_lim = max(max_x_lim, max(args[i][:n+1]))
        max_y_lim = max(max_y_lim, max(args[i+1][:n+1]))
    plt.xlim([min_x_lim - 10, max_x_lim + 10])
    plt.ylim([min_y_lim - 10, max_y_lim + 10])
    for i in range(0, len(args), 6):
        __update(n, args[i], args[i+1], args[i+2], args[i+3], args[i+4], args[i+5])


def draw_history(objects):
    global __N

    n = len(objects[0].x_history)
    __N = n

    fig, ax = plt.subplots()
    ax.grid()

    lines = []
    for obj in objects:
        # print(len(obj.x_history))
        [line] = ax.step(obj.x_history[0], obj.y_history[0])
        [left_border] = ax.step(obj.x_history[0], obj.y_history[0])
        [right_border] = ax.step(obj.x_history[0], obj.y_history[0])
        if obj.type == 'hunter':
            left_border.set_color("#F00")
            right_border.set_color("#F00")
        elif obj.type == 'victim':
            left_border.set_color("#0F0")
            right_border.set_color("#0F0")
        if obj.color:
            line.set_color(obj.color)
        lines.append(line)
        lines.append(left_border)
        lines.append(right_border)

    f_args = []
    for i in range(len(objects)):
        f_args.append(objects[i].x_history)
        f_args.append(objects[i].y_history)
        f_args.append(lines[i * 3])
        f_args.append(lines[i * 3 + 1])
        f_args.append(lines[i * 3 + 2])
        f_args.append(objects[i])
    f_args = tuple(f_args)

    victim = objects[0]
    min_x_lim = victim.x_history[1]
    min_y_lim = victim.y_history[1]
    max_x_lim = victim.x_history[1]
    max_y_lim = victim.y_history[1]
    for hunter in victim.hunters:
        min_x_lim = min(min_x_lim, hunter.x_history[1])
        min_y_lim = min(min_y_lim, hunter.y_history[1])
        max_x_lim = max(max_x_lim, hunter.x_history[1])
        max_y_lim = max(max_y_lim, hunter.y_history[1])
    plt.xlim([min_x_lim - 10, max_x_lim + 10])
    plt.ylim([min_y_lim - 10, max_y_lim + 10])

    anim = animation.FuncAnimation(fig, __update_all, n, fargs=f_args, interval=20, blit=False)
    anim.save('gifs/' + __get_filename(), writer='pillow')
    plt.close()
