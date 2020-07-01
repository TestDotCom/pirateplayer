# pylint: disable=missing-module-docstring
from enum import IntEnum
import logging

from gpiozero import Button

_LOGGER = logging.getLogger(__name__)

_CALLBACKS = [None] * 2
_BUTTONS = [None] * 4


class PlayerState(IntEnum):
    """Player execution states."""
    PLAYING = 0
    BROWSING = 1


def init(pins: list):
    """Setup GPIO buttons."""
    for index, pin in enumerate(pins):
        _BUTTONS[index] = Button(pin)


def set_state(state: PlayerState, handlers: list):
    """Set Player state handlers as callbacks."""
    _CALLBACKS[state] = handlers


def map_buttons(state: PlayerState):
    """Map current-state Buttons to function callbacks."""
    for button, handler in zip(_BUTTONS, _CALLBACKS[state]):
        button.when_pressed = handler
