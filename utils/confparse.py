import configparser
import logging
import os

_LOGGER = logging.getLogger(__name__)

_CONF = configparser.ConfigParser()


def init():
    _LOGGER.setLevel(logging.DEBUG)
    _CONF.read(os.path.expanduser('~/.config/pirateplayer/conf.ini'))


def get_root():
    return os.path.expanduser(_CONF['PLAYER'].get('root', '~/Music'))


def get_pins():
    return list(_CONF['BUTTON'].getint(btn) for btn in _CONF['BUTTON'])
