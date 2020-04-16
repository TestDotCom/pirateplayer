import logging
import os
from signal import pause

from view import View
from inputmap import set_state, map_buttons, PlayerState
from library import Library, Media
from gstreamer import GStreamer


def main():
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.setLevel(logging.DEBUG)

    root = os.path.expanduser('~/Music')
    library = Library(root)

    gst = GStreamer()

    view = View(library.list_files())
    view.display_menu()

    def go_back():
        pass

    def stop_playing():
        gst.stop()
        view.display_menu()

        map_buttons(PlayerState.BROWSING)

    def select():
        media = library.get_file(view.cursor)

        if media is None:
            view.menu = library.list_files()
            view.menulen = len(view.menu)
            view.cursor = 0

            view.display_menu()
        else:
            _LOGGER.debug('path: %s, file: %s', media.path, media.name)

            view.display_track(media.path, media.name)
            gst.run('file://' + media.path + '/' + media.name)

            map_buttons(PlayerState.PLAYING)

    set_state(PlayerState.BROWSING, [view.cursor_up, view.cursor_dwn, select, go_back])
    set_state(PlayerState.PLAYING, [stop_playing, gst.volume_dwn, gst.play, gst.volume_up])

    map_buttons(PlayerState.BROWSING)

    try:
        pause()
    except KeyboardInterrupt:
        _LOGGER.debug('CTRL-C signal')
    finally:
        view.display_clear()
