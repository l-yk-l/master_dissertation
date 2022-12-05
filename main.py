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
            hunter = (self.hunters[-1] + 1) if len(self.hunters) else 1
            self.hunters.append(hunter)
            m = hunter
            self.create_new_label(0, m, str(hunter))

            for i in range(len(self.victims)):
                self.create_new_checkbox(i + 1, m)
        else:
            QtWidgets.QMessageBox().critical(self, "Ошибка", 'Создано максимальное количество объектов "Охотник"',
                                             QtWidgets.QMessageBox.StandardButton.Ok)

    def add_victim(self):
        # global tmp
        #
        # if tmp == 0:
        #     self.ui.canvas.add_object(1)
        #     tmp += 1
        # elif tmp == 1:
        #     self.ui.canvas.add_object(0.5)
        #     tmp += 1
        # else:
        #     self.ui.canvas.add_object(0.1)

        if len(self.victims) < 11:
            dlg = CustomDialog('Добавить жертву')
            if dlg.exec():
                k = float(dlg.sinus_k)
                self.ui.canvas.add_object(k)

                victim = chr(ord(self.victims[-1]) + 1) if len(self.victims) else 'A'
                self.victims.append(victim)
                n = (ord(victim) - ord('A')) + 1
                self.create_new_label(n, 0, victim)

                for i in range(len(self.hunters)):
                    self.create_new_checkbox(n, i + 1)
        else:
            QtWidgets.QMessageBox().critical(self, "Ошибка", 'Создано максимальное количество объектов "Жертва"',
                                             QtWidgets.QMessageBox.StandardButton.Ok)


# Точка входа в программу
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()
