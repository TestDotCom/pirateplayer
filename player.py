import logging
from signal import pause

from view import View
from utils.gstreamer import GStreamer
import utils.inputmap as inputmap
import utils.confparse as confparse
from library import Library


def main():
    """PiratePlayer is built following the
    MVC pattern. This script acts as Controller.
    """
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)

    view = View()

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
            mediapath = 'file://' + media.path + '/' + media.name

            if media.name.endswith(('m3u', 'm3u8')):
                with open(mediapath, 'r') as p:
                    path = 'file://' + media.path + '/'
                    gst.playlist.append(path + track for track in p.readlines())

                track = gst.playlist[0]
            else:
                track = media.name
                gst.playlist.append(mediapath)

            view.display_track(media.path, track)
            gst.run()

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
    finally:
        view.display_clear()
