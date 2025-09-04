from PySide6.QtWidgets import QPushButton
from variables import MEDIUM_FONT_SIZE
from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import Slot
from display import Display
from utils import is_valid_number


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
    def __init__(self, display: Display, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
        self.display = display
        self.make_grid()

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

                self.addWidget(button, i, j)
                button_slot = self.button_display_slot(self.insert_button_text_to_display, button)
                button.clicked.connect(button_slot)

    @staticmethod
    def button_display_slot(func, *args, **kwargs):
        @Slot()
        def real_slot():
            func(*args, **kwargs)

        return real_slot

    def insert_button_text_to_display(self, button: QPushButton):
        button_text = button.text()
        new_display_value = self.display.text() + button_text
        if not is_valid_number(new_display_value):
            print('Aperte uma tecla valida')
        else:
            self.display.insert(button.text())
