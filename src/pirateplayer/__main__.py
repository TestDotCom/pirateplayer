# pylint: disable=missing-module-docstring
import logging
from signal import pause

from pirateplayer.view import View
from pirateplayer.utils.gstreamer import GStreamer
import pirateplayer.utils.confparse as confparse
from pirateplayer.library import Library
from pirateplayer.controller import Controller


def main():
    """PiratePlayer entrypoint: 
    initialize components and 
    assemble dependencies.
    """
    logging.basicConfig(level=logging.DEBUG)

    confparse.init()
    pins = confparse.get_pins()
    root = confparse.get_root()

    model = Library(root)
    view = View()
    player = GStreamer()
    
    Controller(view, model, player, pins)

    pause()
