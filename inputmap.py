from enum import Enum
import logging

from gpiozero import Button

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

_CALLBACKS = [None] * 2

_BUTTONS = [
    Button(5),  # A
    Button(6),  # B
    Button(16),  # X
    Button(20)  # Y
]


class PlayerState:
    PLAYING = 0
    BROWSING = 1


def set_state(state, handlers):
    _CALLBACKS[state] = handlers


def map_buttons(state):
    for button, handler in zip(_BUTTONS, _CALLBACKS[state]):
        button.when_pressed = handler
