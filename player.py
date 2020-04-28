import configparser
import logging
import os
from signal import pause

from view import View
from inputmap import PlayerState, set_buttons, set_state, map_buttons
from library import Library
from gstreamer import GStreamer


def main():
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.setLevel(logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('conf.ini')

    root = os.path.expanduser(config['PLAYER'].get('root', '~/Music'))
    library = Library(root)

    view = View()
    view.display_logo()

    gst = GStreamer()

    def go_back():
        library.get_previous()
        menu = library.list_files()

        view.update_menu(menu)
        view.display_menu()

    def select():
        media = library.get_next(view.cursor)

        if media is None:
            menu = library.list_files()

            view.update_menu(menu)
            view.display_menu()
        else:
            _LOGGER.debug('path: %s, file: %s', media.path, media.name)

            view.display_track(media.path, media.name)
            gst.run('file://' + media.path + '/' + media.name)

            map_buttons(PlayerState.PLAYING)

    def stop_playing():
        gst.stop()
        view.display_menu()

        map_buttons(PlayerState.BROWSING)

    set_state(
        PlayerState.BROWSING, [
            view.cursor_up, view.cursor_dwn, select, go_back])
    set_state(
        PlayerState.PLAYING, [
            stop_playing, gst.volume_dwn, gst.play, gst.volume_up])

    buttons = list(config['BUTTON'].getint(btn) for btn in config['BUTTON'])
    set_buttons(buttons)
    map_buttons(PlayerState.BROWSING)

    view.update_menu(library.list_files())
    view.display_menu()

    try:
        pause()
    except KeyboardInterrupt:
        _LOGGER.debug('CTRL-C signal')
    finally:
        view.display_clear()
