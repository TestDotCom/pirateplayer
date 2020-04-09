import logging

from gpiozero import Button

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger('input')


class Input:
    def __init__(self):
        self.__buttons = [
            Button(5),  # A
            Button(6),  # B
            Button(16),  # X
            Button(20)  # Y
        ]

    def setup(self, handlers):
        for button, handler in zip(self.__buttons, handlers):
            button.when_pressed = handler
