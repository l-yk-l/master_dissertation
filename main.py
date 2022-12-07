import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from interface import Ui_MainWindow
from interface import CustomDialog


# Класс для катомизации главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Инициализируем интерфейс из interface.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Массивы охотников и жертв
        self.hunters = []
        self.victims = []
        # Массивы лейблов охотников и жертв
        self.hunter_lbls = []
        self.victim_lbls = []
        # Привязываем методы добавления объектов к кнопкам
        self.ui.addHunterBtn.clicked.connect(self.add_hunter)
        self.ui.addVictimBtn.clicked.connect(self.add_victim)

        # Вызываем наше окно
        self.show()

    # Метод для привязки и отвязки охотников к/от жертв(ам)
    # Срабатывает при изменении любого чекбокса
    def attach_detach_hunter_victim(self, row, col):
        # Получаем данные с чекбокса (его положение и значение)
        checkbox = self.findChild(QtWidgets.QCheckBox, f"checkBox_{row}_{col}")
        state = checkbox.isChecked()
        # ------------------------------------------------
        # Some code to attach/detach Hunter to/from Victim
        # ------------------------------------------------

    # Метод создания нового чекбокса по номеру строки и столбца
    def create_new_checkbox(self, row, col):
        # Создаем и стилизуем чекбокс
        checkbox = QtWidgets.QCheckBox(self.ui.gridLayoutWidget)
        checkbox.setObjectName(f"checkBox_{row}_{col}")
        checkbox.stateChanged.connect(lambda: self.attach_detach_hunter_victim(row, col))
        checkbox.setStyleSheet("""
            QCheckBox::indicator
            {
                width :15px;
                height : 15px;
            }
        """)
        # Помещаем новый чекбокс на наше окно
        self.ui.gridLayout.addWidget(checkbox, row, col, 1, 1)

    # Метод создания нового лейбла (по сути отображение имени объекта в матрице чекбоксов)
    # Также нужно передать номера строки и столбца, а так же текст лейбла
    def create_new_label(self, n, m, lbl_text):
        # Создаем и стилизуем лейбл
        label = QtWidgets.QLabel(self.ui.gridLayoutWidget)
        label.setObjectName(f"label_{lbl_text}")
        label.setText(str(lbl_text))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        font = QtGui.QFont()
        font.setPointSize(11)
        label.setFont(font)
        # Помещаем новый лейбл на наше окно
        self.ui.gridLayout.addWidget(label, n, m, 1, 1)

    def add_hunter(self):
        if len(self.hunters) < 11:
            dlg = CustomDialog('hunter')
            if dlg.exec():
                v_start_x = dlg.start_x
                v_start_y = dlg.start_y
                v_direction = dlg.direction
                v_speed = dlg.speed
                v_max_angle_of_rotation = dlg.max_angle_of_rotation
                v_angle_of_vision = dlg.angle_of_vision
                v_len_of_vision = dlg.len_of_vision

                hunter = self.ui.canvas.add_object('hunter', v_start_x, v_start_y, v_direction, v_speed,
                                                   v_max_angle_of_rotation,
                                                   v_angle_of_vision, v_len_of_vision)
                self.hunters.append(hunter)

                hunter_lbl = (self.hunter_lbls[-1] + 1) if len(self.hunter_lbls) else 1
                self.hunter_lbls.append(hunter_lbl)
                m = hunter_lbl
                self.create_new_label(0, m, str(hunter_lbl))

                for i in range(len(self.victims)):
                    self.create_new_checkbox(i + 1, m)
        else:
            QtWidgets.QMessageBox().critical(self, "Ошибка", 'Создано максимальное количество объектов "Охотник"',
                                             QtWidgets.QMessageBox.StandardButton.Ok)

    def add_victim(self):
        if len(self.victims) < 11:
            dlg = CustomDialog('victim')
            if dlg.exec():
                v_start_x = dlg.start_x
                v_start_y = dlg.start_y
                v_direction = dlg.direction
                v_speed = dlg.speed
                v_max_angle_of_rotation = dlg.max_angle_of_rotation
                v_angle_of_vision = dlg.angle_of_vision
                v_len_of_vision = dlg.len_of_vision

                victim = self.ui.canvas.add_object('victim', v_start_x, v_start_y, v_direction, v_speed,
                                                   v_max_angle_of_rotation,
                                                   v_angle_of_vision, v_len_of_vision)
                self.victims.append(victim)

                victim_lbl = chr(ord(self.victim_lbls[-1]) + 1) if len(self.victim_lbls) else 'A'
                self.victim_lbls.append(victim_lbl)
                n = (ord(victim_lbl) - ord('A')) + 1
                self.create_new_label(n, 0, victim_lbl)

                for i in range(len(self.hunters)):
                    self.create_new_checkbox(n, i + 1)
        else:
            QtWidgets.QMessageBox().critical(self, "Ошибка", 'Создано максимальное количество объектов "Жертва"',
                                             QtWidgets.QMessageBox.StandardButton.Ok)


# Точка входа в программу
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

    #
    victim = w.ui.canvas.add_object('victim', v_start_x=0, v_start_y=0, v_direction=30, v_speed=0.3,
                                    v_max_angle_of_rotation=45, v_angle_of_vision=30, v_len_of_vision=10)
    w.victims.append(victim)

    victim_lbl = chr(ord(w.victim_lbls[-1]) + 1) if len(w.victim_lbls) else 'A'
    w.victim_lbls.append(victim_lbl)
    n = (ord(victim_lbl) - ord('A')) + 1
    w.create_new_label(n, 0, victim_lbl)

    #
    hunter = w.ui.canvas.add_object('hunter', v_start_x=-4, v_start_y=2, v_direction=-10, v_speed=0.5,
                                    v_max_angle_of_rotation=10, v_angle_of_vision=30, v_len_of_vision=10)
    w.hunters.append(hunter)

    hunter_lbl = (w.hunter_lbls[-1] + 1) if len(w.hunter_lbls) else 1
    w.hunter_lbls.append(hunter_lbl)
    m = hunter_lbl
    w.create_new_label(0, m, str(hunter_lbl))

    for i in range(len(w.victims)):
        w.create_new_checkbox(i + 1, m)

    app.exec()
