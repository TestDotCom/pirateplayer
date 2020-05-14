# pylint: disable=missing-module-docstring
from enum import IntEnum
import logging

from gpiozero import Button
import pirateplayer.utils.confparse as confparse

_LOGGER = logging.getLogger(__name__)

_CALLBACKS = [None] * 2
_BUTTONS = [None] * 4


class PlayerState(IntEnum):
    """Player execution states."""
    PLAYING = 0
    BROWSING = 1


def init():
    """Setup GPIO buttons."""
    for index, pin in enumerate(confparse.get_pins()):
        _BUTTONS[index] = Button(pin)


def set_state(state, handlers):
    """Switch Player current-state."""
    _CALLBACKS[state] = handlers


def map_buttons(state):
    """Map current-state Buttons to function callbacks."""
    for button, handler in zip(_BUTTONS, _CALLBACKS[state]):
        button.when_pressed = handler
