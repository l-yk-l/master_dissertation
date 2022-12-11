import numpy as np
import math, time, random
from collections import deque


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


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
        self.plt.xlim([-10.6, 10.6])
        self.plt.ylim([-10.6, 10.6])
        self.objects = []

    def update(self, dy):
        # pass
        # last = self.x[-1]
        if not self.isPaused:
            if len(self.objects) >= 1:
                obj = self.objects[0]
                # print(obj.x)
                mn_x = min(obj.x)
                mx_x = max(obj.x)
                mn_y = min(obj.y)
                mx_y = max(obj.y)
                for i in range(1, len(self.objects)):
                    obj = self.objects[i]
                    mn_x = min(mn_x, min(obj.x))
                    mx_x = max(mx_x, max(obj.x))
                    mn_y = min(mn_y, min(obj.y))
                    mx_y = max(mx_y, max(obj.y))
                x_perc = (mx_x - mn_x) / 10
                y_perc = (mx_y - mn_y) / 10
                self.plt.xlim([mn_x - x_perc, mx_x + x_perc])
                self.plt.ylim([mn_y - y_perc, mx_y + y_perc])
            else:
                self.plt.xlim([-10.6, 10.6])
                self.plt.ylim([-10.6, 10.6])
        #     self.x.append(last + self.e)  # update data
        #     self.y.append(dy)
        #     self.x_history.append(last + self.e)
        #     self.y_history.append(dy)
        #
        #     self.line.set_xdata(self.x)  # update plot data
        #     self.line.set_ydata(self.y)
        #
        #     # лимиты осей (с какой по какую точку оси отображать плот)
        #     # if last < 10:
        #     #     self.plt.xlim([-0.6, 10.6])
        #     # else:
        #     #     self.plt.xlim([last - 10.6, last + 0.6])
        #     # self.plt.ylim([-1.2, 1.2])
        #     self.ax.autoscale_view(True, True, True)
        #
        #     return self.line, self.ax

    def data_gen(self):
        while True:
            yield np.sin(self.k * np.pi * self.x[-1])

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)


class Victim(object):
    def __init__(self, plt, ax, start_x, start_y, direction, speed, max_angle_of_rotation, angle_of_vision, len_of_vision, n_points=500):
        self.type = "victim"
        self.n_points = n_points
        self.e = 10 / n_points
        self.direction = direction
        self.speed = speed
        self.max_angle_of_rotation = max_angle_of_rotation
        npx = np.array([start_x-0.1, start_x])
        npy = np.array([start_y-0.1, start_y])
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(npy, maxlen=n_points)
        self.x_history = [self.x[0], self.x[1]]
        self.y_history = [self.y[0], self.y[1]]
        self.hunters = []
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.vision_left_border_x = None
        self.vision_left_border_y = None
        self.vision_right_border_x = None
        self.vision_right_border_y = None
        self.angle_of_vision = angle_of_vision
        self.len_of_vision = len_of_vision
        [self.left_border] = self.ax.step(self.x, self.y)
        [self.right_border] = self.ax.step(self.x, self.y)
        self.left_border.set_color('green')
        self.right_border.set_color('green')
        self.draw_vision()
        self.color = None
        #
        # self.plt.xlim([self.x[-1]-10, self.x[-1]+10])
        # self.plt.ylim([self.y[-1]-10, self.y[-1]+10])

    def update(self, dy):
        # A(x1, y1)
        # a - угол в градусах
        # d - расстояние
        # B = (x1 + d*cos(a), y1 + d*sin(a))
        if not self.isPaused:
            # Расчет угла поворота
            if len(self.hunters) and self.view_hunter():
                min_rotation = 181
                current_hunter_x = None
                current_hunter_y = None
                for hunter in self.hunters:
                    s_x = hunter.x[-1] - self.x[-1]
                    s_y = hunter.y[-1] - self.y[-1]
                    sin_fi = np.cos(np.radians(self.direction))
                    cos_fi = np.sin(np.radians(self.direction))
                    local_hunter_x = s_x * sin_fi + s_y * cos_fi
                    local_hunter_y = -s_x * cos_fi + s_y * sin_fi
                    if current_hunter_x is None:
                        current_hunter_x = local_hunter_x
                    if current_hunter_y is None:
                        current_hunter_y = local_hunter_y
                    # print(f"x = {local_hunter_x}; y = {local_hunter_y}")
                    angle_from_hunter = 0
                    if local_hunter_x:
                        angle_from_hunter = np.degrees(np.arctan(local_hunter_y / local_hunter_x))
                    else:
                        angle_from_hunter = np.sign(local_hunter_y) * 90.0

                    if abs(angle_from_hunter) < min_rotation:
                        min_rotation = angle_from_hunter
                        current_hunter_x = local_hunter_x
                        current_hunter_y = local_hunter_y

                    was_rabbit_jump = self.rabbit_jump(hunter)
                # print(min_rotation)
                if not was_rabbit_jump:
                    if current_hunter_y < 0:
                        self.direction += min(self.max_angle_of_rotation, abs(min_rotation))
                    else:
                        self.direction -= min(self.max_angle_of_rotation, abs(min_rotation))

            for i in range(10):
                last_x = self.x[-1]
                last_y = self.y[-1]
                self.x.append(last_x + (self.speed/10) * np.cos(np.radians(self.direction)))
                self.y.append(last_y + (self.speed/10) * np.sin(np.radians(self.direction)))
                self.x_history.append(self.x[-1])
                self.y_history.append(self.y[-1])

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)
            self.draw_vision()

            # print(self.direction, 180+self.direction, 180+self.direction - (self.angle_of_vision / 2),
            #       180+self.direction + (self.angle_of_vision / 2))

            # лимиты осей (с какой по какую точку оси отображать плот)
            self.set_plt_lims()
            self.ax.autoscale_view(True, True, True)

            time.sleep(0.05)

            return self.line, self.ax

    # Отрисовка конуса слежения
    def draw_vision(self):
        # Расчет координат точек конуса обзора
        self.vision_left_border_x = self.x[-1] + self.len_of_vision * np.cos(
            np.radians(180+self.direction - (self.angle_of_vision / 2)))
        self.vision_left_border_y = self.y[-1] + self.len_of_vision * np.sin(
            np.radians(180+self.direction - (self.angle_of_vision / 2)))
        self.vision_right_border_x = self.x[-1] + self.len_of_vision * np.cos(
            np.radians(180+self.direction + (self.angle_of_vision / 2)))
        self.vision_right_border_y = self.y[-1] + self.len_of_vision * np.sin(
            np.radians(180+self.direction + (self.angle_of_vision / 2)))
        self.left_border.set_xdata(np.linspace(self.x[-1], self.vision_left_border_x, math.ceil(self.len_of_vision) * 6))
        self.left_border.set_ydata(np.linspace(self.y[-1], self.vision_left_border_y, math.ceil(self.len_of_vision) * 6))
        self.right_border.set_xdata(np.linspace(self.x[-1], self.vision_right_border_x, math.ceil(self.len_of_vision) * 6))
        self.right_border.set_ydata(np.linspace(self.y[-1], self.vision_right_border_y, math.ceil(self.len_of_vision) * 6))

    # return bool
    # Видит ли жертва охотника
    # 1, 2, 3 - вершины треугольника слежения; 0 - текущие корды жертвы
    # t1 = (x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0)
    # t2 = (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0)
    # t3 = (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0)
    # если sign(t1) == sign(t2) == sign(t3) - точка внутри треугольника
    # если t1 == 0 or t2 == 0 or t3 == 0 - точка на границе треугольника
    # иначе точка вне треугольника
    def view_hunter(self):
        for hunter in self.hunters:
            x1 = self.x[-1]
            y1 = self.y[-1]
            x2 = self.vision_left_border_x
            y2 = self.vision_left_border_y
            x3 = self.vision_right_border_x
            y3 = self.vision_right_border_y
            x0 = hunter.x[-1]
            y0 = hunter.y[-1]

            t1 = np.sign((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0))
            t2 = np.sign((x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0))
            t3 = np.sign((x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0))

            if t1 * t2 * t3 == 0 or (t1 == t2 and t2 == t3):
                return True

        return False

    def rabbit_jump(self, hunter):
        distance = get_distance(self.x[-1], self.y[-1], hunter.x[-1], hunter.y[-1])
        if distance < hunter.speed:
            self.direction += (1 if random.random() < 0.5 else -1) * self.max_angle_of_rotation
            return

    def stop_all(self):
        self.isPaused = True
        for hunter in self.hunters:
            hunter.isPaused = True

    def set_plt_lims(self):
        min_x_lim = min(self.x)
        min_y_lim = min(self.y)
        max_x_lim = max(self.x)
        max_y_lim = max(self.y)
        # for hunter in self.hunters:
        #     min_x_lim = min(min_x_lim, min(hunter.x))
        #     min_y_lim = min(min_y_lim, min(hunter.y))
        #     max_x_lim = max(max_x_lim, max(hunter.x))
        #     max_y_lim = max(max_y_lim, max(hunter.y))
        # self.plt.xlim([min_x_lim-10, max_x_lim+10])
        # self.plt.ylim([min_y_lim - 10, max_y_lim + 10])

    def data_gen(self):
        while True:
            yield self.y[-1]

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)

    def add_hunter(self, hunter):
        self.hunters.append(hunter)

    def remove_hunter(self, hunter):
        if hunter in self.hunters:
            ind = self.hunters.index(hunter)
            self.hunters = self.hunters[:ind] + self.hunters[ind+1:]


class Hunter(object):
    def __init__(self, plt, ax, start_x, start_y, direction, speed, max_angle_of_rotation, angle_of_vision, len_of_vision, n_points=500):
        self.type = "hunter"
        self.n_points = n_points
        self.e = 10 / n_points
        self.direction = direction
        self.speed = speed
        self.max_angle_of_rotation = max_angle_of_rotation
        npx = np.array([start_x-0.1, start_x])
        npy = np.array([start_y-0.1, start_y])
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(npy, maxlen=n_points)
        self.x_history = [self.x[0], self.x[1]]
        self.y_history = [self.y[0], self.y[1]]
        self.victims = []
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.vision_left_border_x = None
        self.vision_left_border_y = None
        self.vision_right_border_x = None
        self.vision_right_border_y = None
        self.angle_of_vision = angle_of_vision
        self.len_of_vision = len_of_vision
        [self.left_border] = self.ax.step(self.x, self.y)
        [self.right_border] = self.ax.step(self.x, self.y)
        self.left_border.set_color('red')
        self.right_border.set_color('red')
        self.draw_vision()
        self.color = None

    def update(self, dy):
        # A(x1, y1)
        # a - угол в градусах
        # d - расстояние
        # B = (x1 + d*cos(a), y1 + d*sin(a))
        if not self.isPaused:
            if len(self.victims):
                victim = self.victims[0]
                mn_range = get_distance(self.x[-1], self.y[-1], victim.x[-1], victim.y[-1])
                for obj in self.victims:
                    cur_range = get_distance(self.x[-1], self.y[-1], obj.x[-1], obj.y[-1])
                    if cur_range < mn_range:
                        mn_range = cur_range
                        victim = obj
                # Расчет угла поворота
                if self.view_victim(victim):
                    s_x = victim.x[-1] - self.x[-1]
                    s_y = victim.y[-1] - self.y[-1]
                    sin_fi = np.cos(np.radians(self.direction))
                    cos_fi = np.sin(np.radians(self.direction))

                    local_victim_x = s_x * sin_fi + s_y * cos_fi
                    local_victim_y = -s_x * cos_fi + s_y * sin_fi
                    # print(f"x = {local_victim_x}; y = {local_victim_y}")
                    angle_to_victim = 0
                    if local_victim_x:
                        angle_to_victim = np.degrees(np.arctan(local_victim_y / local_victim_x))
                    else:
                        angle_to_victim = np.sign(local_victim_y) * 90.0

                    if local_victim_y > 0:
                        self.direction += min(self.max_angle_of_rotation, abs(angle_to_victim))
                    else:
                        self.direction -= min(self.max_angle_of_rotation, abs(angle_to_victim))

            for i in range(10):
                last_x = self.x[-1]
                last_y = self.y[-1]
                self.x.append(last_x + (self.speed/10) * np.cos(np.radians(self.direction)))
                self.y.append(last_y + (self.speed/10) * np.sin(np.radians(self.direction)))
                self.x_history.append(self.x[-1])
                self.y_history.append(self.y[-1])

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)
            self.draw_vision()

            self.ax.autoscale_view(True, True, True)
            return self.line, self.ax

    # Отрисовка конуса слежения
    def draw_vision(self):
        # Расчет координат точек конуса обзора
        self.vision_left_border_x = self.x[-1] + self.len_of_vision * np.cos(np.radians(self.direction - (self.angle_of_vision / 2)))
        self.vision_left_border_y = self.y[-1] + self.len_of_vision * np.sin(np.radians(self.direction - (self.angle_of_vision / 2)))
        self.vision_right_border_x = self.x[-1] + self.len_of_vision * np.cos(np.radians(self.direction + (self.angle_of_vision / 2)))
        self.vision_right_border_y = self.y[-1] + self.len_of_vision * np.sin(np.radians(self.direction + (self.angle_of_vision / 2)))

        self.left_border.set_xdata(np.linspace(self.x[-1], self.vision_left_border_x, math.ceil(self.len_of_vision)*6))
        self.left_border.set_ydata(np.linspace(self.y[-1], self.vision_left_border_y, math.ceil(self.len_of_vision)*6))
        self.right_border.set_xdata(np.linspace(self.x[-1], self.vision_right_border_x, math.ceil(self.len_of_vision)*6))
        self.right_border.set_ydata(np.linspace(self.y[-1], self.vision_right_border_y, math.ceil(self.len_of_vision)*6))

    # return bool
    # Видит ли охотник жертву
    # 1, 2, 3 - вершины треугольника слежения; 0 - текущие корды жертвы
    # t1 = (x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0)
    # t2 = (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0)
    # t3 = (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0)
    # если sign(t1) == sign(t2) == sign(t3) - точка внутри треугольника
    # если t1 == 0 or t2 == 0 or t3 == 0 - точка на границе треугольника
    # иначе точка вне треугольника
    def view_victim(self, victim):
        x1 = self.x[-1]
        y1 = self.y[-1]
        x2 = self.vision_left_border_x
        y2 = self.vision_left_border_y
        x3 = self.vision_right_border_x
        y3 = self.vision_right_border_y
        x0 = victim.x[-1]
        y0 = victim.y[-1]

        t1 = np.sign((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0))
        t2 = np.sign((x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0))
        t3 = np.sign((x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0))

        # t1 = np.sign((self.x[-1] - self.victim.x[-1]) * (self.vision_left_border_y - self.y[-1]) - (self.vision_left_border_x - self.x[-1]) * (self.y[-1] - self.victim.y[-1]))
        # t2 = np.sign((self.vision_left_border_x - self.victim.x[-1]) * (self.vision_right_border_y - self.vision_left_border_y) - (self.vision_right_border_x - self.vision_left_border_x) * (self.vision_left_border_y - self.victim.y[-1]))
        # t3 = np.sign((self.vision_right_border_x - self.victim.x[-1]) * (self.y[-1] - self.vision_right_border_y) - (self.x[-1] - self.vision_right_border_x) * (self.vision_right_border_y - self.victim.y[-1]))

        if t1 * t2 * t3 == 0 or (t1 == t2 and t2 == t3):
            return True
        return False

    def data_gen(self):
        while True:
            yield self.y[-1]

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)

    def add_victim(self, victim):
        self.victims.append(victim)

    def remove_victim(self, victim):
        if victim in self.victims:
            ind = self.victims.index(victim)
            self.victims = self.victims[:ind] + self.victims[ind+1:]
