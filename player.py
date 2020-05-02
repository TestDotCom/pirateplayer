import logging
from signal import pause

from view import View
from utils.gstreamer import GStreamer
import utils.inputmap as inputmap
import utils.confparse as confparse
from library import Library


def main():
    """Tie together each other piece of software.
    Setup music folder and buttons pin number,
    index music library and start gstreamer.
    """
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)

    view = View()
    view.display_logo()

    confparse.init()
    inputmap.init()

    library = Library()
    gst = GStreamer()

    def go_back():
        library.get_previous()
        menu = library.list_files()

        view.update_menu(menu)
        view.display_menu()

    def select():
        media = library.get_next(view.cursor)
        _logger.debug('path: %s, file: %s', media.path, media.name)

        if media.isdir:
            menu = library.list_files()

            view.update_menu(menu)
            view.display_menu()
        else:
            if media.name.endswith(('m3u', 'm3u8')):
                pass
            else:
                view.display_track(media.path, media.name)
                gst.run('file://' + media.path + '/' + media.name)

            inputmap.map_buttons(inputmap.PlayerState.PLAYING)

    def stop_playing():
        gst.stop()
        view.display_menu()

        inputmap.map_buttons(inputmap.PlayerState.BROWSING)

    inputmap.set_state(
        inputmap.PlayerState.BROWSING, [
            view.cursor_up, view.cursor_dwn, select, go_back])

    inputmap.set_state(
        inputmap.PlayerState.PLAYING, [
            stop_playing, gst.volume_dwn, gst.play, gst.volume_up])

    inputmap.map_buttons(inputmap.PlayerState.BROWSING)

    view.update_menu(library.list_files())
    view.display_menu()

    try:
        pause()
    except KeyboardInterrupt:
        _logger.debug('CTRL-C signal')
        view.display_clear()
