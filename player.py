import logging
import os
from signal import pause

from display import display_clear, display_track, display_menu
from inputmap import map_buttons
from library import make_index, list_files
from gstreamer import GStreamer

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)


def main():
    def move_up():
        pass

    def move_dwn():
        pass

    def select():
        pass

    def go_back():
        pass

    try:
        #gst = GStreamer()
        #map_buttons([None, gst.play, None, None])

        #gst.run('file:///usr/share/sounds/alsa/Front_Center.wav')

        current_dir = os.path.expanduser('~/Music')
        make_index(current_dir)

        display_menu(list_files(current_dir))

        pause()
    except KeyboardInterrupt:
        _LOGGER.debug('CTRL-C signal')
    finally:
        display_clear()
