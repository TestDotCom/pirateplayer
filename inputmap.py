import logging

from gpiozero import Button

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

_CALLBACKS = [None] * 2
_BUTTONS = [None] * 4


class PlayerState:
    PLAYING = 0
    BROWSING = 1


def set_buttons(pins):
    for index, pin in enumerate(pins):
        _BUTTONS[index] = Button(pin)


def set_state(state, handlers):
    _CALLBACKS[state] = handlers


def map_buttons(state):
    for button, handler in zip(_BUTTONS, _CALLBACKS[state]):
        button.when_pressed = handler
