import logging
import os
from signal import pause

from view import View
from inputmap import map_buttons
from library import make_index, list_files
from gstreamer import GStreamer


def main():
    logging.basicConfig(level=logging.DEBUG)
    _LOGGER = logging.getLogger(__name__)

    gst = GStreamer()

    current_dir = os.path.expanduser('~/Music')
    make_index(current_dir)

    filenames = list_files(current_dir)
    
    view = View(filenames)
    view.display_menu()

    def select():
        _LOGGER.debug(f'track selected: {filenames[view.cursor]}')


    def go_back():
        pass

    def next_track():
        pass

    def previous_track():
        pass

    def handle_play():
        pass

    map_buttons([view.cursor_up, view.cursor_dwn, select, go_back])

    try:
        pause()
    except KeyboardInterrupt:
        _LOGGER.debug('CTRL-C signal')
    finally:
        view.display_clear()
