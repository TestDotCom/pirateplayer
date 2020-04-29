from enum import Enum
import logging

from gpiozero import Button

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

_CALLBACKS = [None] * 2
_BUTTONS = [None] * 4


class PlayerState(Enum):
    """Player execution states."""
    PLAYING = 0
    BROWSING = 1


def set_buttons(pins):
    """Map pins to button objects"""
    for index, pin in enumerate(pins):
        _BUTTONS[index] = Button(pin)


def set_state(state, handlers):
    """Change Player current state."""
    _CALLBACKS[state] = handlers


def map_buttons(state):
    """Map this {state} Buttons to function callbacks."""
    for button, handler in zip(_BUTTONS, _CALLBACKS[state]):
        button.when_pressed = handler
