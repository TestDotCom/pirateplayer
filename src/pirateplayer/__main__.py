# pylint: disable=missing-module-docstring
import logging

from pirateplayer.view import View
from pirateplayer.utils.gstreamer import GStreamer
import pirateplayer.utils.inputmap as inputmap
import pirateplayer.utils.confparse as confparse
from pirateplayer.library import Library
from pirateplayer.controller import Controller


def main():
    """PiratePlayer entrypoint: initialize components."""
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pykka').setLevel(logging.INFO)

    confparse.init()
    inputmap.init()

    view = View()
    model = Library()
    player = GStreamer()

    Controller.start(view, model, player)
