from PySide6.QtWidgets import QPushButton
from variables import MEDIUM_FONT_SIZE
from PySide6.QtWidgets import QGridLayout


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
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
