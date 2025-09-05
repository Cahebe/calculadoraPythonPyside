from PySide6.QtWidgets import QPushButton
from variables import MEDIUM_FONT_SIZE
from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import Slot
from display import Display
from utils import is_valid_number
from info import Info
from math import pow


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
    def __init__(self, display: Display, info: Info, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
        self.display = display
        self.info = info
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
        for i, row in enumerate(self._grid_mask):
            for j, button_text in enumerate(row):
                button = Button(button_text)
                if button_text == '':
                    continue

                if button_text == '0':
                    self.addWidget(button, i, j, 1, 2)

                if button_text not in '0123456789.':
                    button.setProperty('cssClass', '')
                    self.config_special_button(button)

                self.addWidget(button, i, j)
                button_slot = self._make_slot(self.insert_button_text_to_display, button)
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
        if text in "+-/*^":
            self.connect_button_clicked(button, self._make_slot(self.operator_clicked, button))
        if text == "=":
            self.connect_button_clicked(button, self._equal)

    @staticmethod
    def _make_slot(func, *args, **kwargs):
        @Slot()
        def real_slot():
            func(*args, **kwargs)

        return real_slot

    def insert_button_text_to_display(self, button):
        button_text = button.text()
        new_display_value = self.display.text() + button_text
        if not is_valid_number(new_display_value):
            return
        else:
            self.display.insert(button.text())

    def _clear(self):
        self.left_number = None
        self.right_number = None
        self.operator = None
        self.equation = self.equationInitialValue
        self.display.clear()

    def operator_clicked(self, button):
        button_text = button.text()
        display_text = self.display.text()
        self.display.clear()

        if not is_valid_number(display_text) and self.left_number is None:
            return

        if self.left_number is None:
            self.left_number = float(display_text)

        self.operator = button_text
        self.equation = f'{self.left_number} {self.operator} '

    def _equal(self):
        display_text = self.display.text()
        if not is_valid_number(display_text):
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
            msg = 'Não se pode dividir por 0'
            self.display.clear()
            self.info.setText(msg)
            return

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self.left_number = result
        self.right_number = None
