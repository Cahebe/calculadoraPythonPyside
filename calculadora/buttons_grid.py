from PySide6.QtWidgets import QPushButton
from variables import MEDIUM_FONT_SIZE
from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import Slot
from display import Display
from utils import is_valid_number
from info import Info
from math import pow
from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        self.setProperty('cssClass', 'specialButton')


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['-n', '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self.equation = ''
        self.equationInitialValue = '0'
        self.left_number = None
        self.right_number = None
        self.operator = None
        self.equation = self.equationInitialValue
        self.make_grid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def make_grid(self):
        self.display.eq_pressed.connect(self._equal)
        self.display.del_pressed.connect(self.display.backspace)
        self.display.clear_pressed.connect(self._clear)
        self.display.input_pressed.connect(self.insert_button_text_to_display)
        self.display.operator_pressed.connect(self.operator_clicked)

        for i, row in enumerate(self._grid_mask):
            for j, button_text in enumerate(row):
                button = Button(button_text)
                if button_text == '':
                    continue

                # if button_text == '0':
                #     self.addWidget(button, i, j, 1, 2)

                # if button_text == '-n':
                #     self.addWidget(button, i, j)

                if button_text not in '0123456789.':
                    button.setProperty('cssClass', '')
                    self.config_special_button(button)

                self.addWidget(button, i, j)
                button_slot = self._make_slot(self.insert_button_text_to_display, button_text)
                self.connect_button_clicked(button, button_slot)

    @staticmethod
    def connect_button_clicked(button, slot):
        button.clicked.connect(slot)

    def config_special_button(self, button: QPushButton):
        text = button.text()
        if text == "C":
            self.connect_button_clicked(button, self._clear)
        if text == "◀":
            self.connect_button_clicked(button, self.display.backspace)
        if text in "+-/^":
            self.connect_button_clicked(button, self._make_slot(self.operator_clicked, text))
        if text == "=":
            self.connect_button_clicked(button, self._equal)
        if text == "-n":
            self.connect_button_clicked(button, self.invert_number)

    @staticmethod
    def _make_slot(func, *args, **kwargs):
        @Slot()
        def real_slot():
            func(*args, **kwargs)

        return real_slot

    @Slot()
    def insert_button_text_to_display(self, text):
        new_display_value = self.display.text() + text
        if not is_valid_number(new_display_value):
            return
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self.left_number = None
        self.right_number = None
        self.operator = None
        self.equation = self.equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def operator_clicked(self, text):
        display_text = self.display.text()
        self.display.clear()

        if not is_valid_number(display_text) and self.left_number is None:
            return

        if self.left_number is None:
            self.left_number = float(display_text)

        self.operator = text
        self.equation = f'{self.left_number} {self.operator} '
        self.display.setFocus()

    @Slot()
    def _equal(self):
        display_text = self.display.text()
        if not is_valid_number(display_text) or self.left_number is None:
            self._show_error('Conta incompleta.')
            return

        self.right_number = float(display_text)
        self.equation = f'{self.left_number} {self.operator} {self.right_number}'

        result = 0.0
        try:
            if '^' in self.equation:
                result = pow(self.left_number, self.right_number)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._show_error('Não se pode dividir por 0')
            self.display.clear()
            return

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self.left_number = result
        self.right_number = None

        self.display.setFocus()

    def _show_error(self, text):
        msg_box = self.window.make_msg_box()
        msg_box.setText(text)
        msg_box.setIcon(msg_box.Icon.Warning)
        msg_box.exec()

    @Slot()
    def invert_number(self):
        display_text = self.display.text()

        if not is_valid_number(display_text):
            return

        new_number = float(display_text) * -1
        self.display.setText(str(new_number))
