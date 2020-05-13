# pylint: disable=missing-module-docstring
import configparser
import logging
import os

_LOGGER = logging.getLogger(__name__)
_CONF = configparser.ConfigParser()


def init():
    """Read configuration file"""
    _CONF.read(os.path.expanduser('~/.config/pirateplayer/conf.ini'))


def get_root():
    """Return user-defined music directory,
    or default path if none specified.
    """
    return os.path.expanduser(_CONF['PLAYER'].get('root', '~/Music'))


def get_pins():
    """Return user-defined buttons pin."""
    return list(_CONF['BUTTON'].getint(btn) for btn in _CONF['BUTTON'])
