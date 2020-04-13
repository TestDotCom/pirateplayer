import logging

from gpiozero import Button

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

_buttons = [
    Button(5),  # A
    Button(6),  # B
    Button(16),  # X
    Button(20)  # Y
]


def map_buttons(handlers):
    for button, handler in zip(_buttons, handlers):
        button.when_pressed = handler
