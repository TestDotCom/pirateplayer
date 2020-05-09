import logging

from view import View
from utils.gstreamer import GStreamer
import utils.inputmap as inputmap
import utils.confparse as confparse
from library import Library
from controller import Controller

def main():
    """PiratePlayer entrypoint: initialize components."""
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pykka').setLevel(logging.INFO)

    confparse.init()
    inputmap.init()

    view = View().start().proxy()
    model = Library().start().proxy()
    player = GStreamer()

    Controller.start(view, model, player)
