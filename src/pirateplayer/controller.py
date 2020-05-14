# pylint: disable=missing-module-docstring
import logging
from pykka import ThreadingActor

import pirateplayer.utils.inputmap as inputmap


class Controller(ThreadingActor):
    """MVC design pattern -> Control actor.
    Responsible for coordinating each other actor.
    """

    def __init__(self, view, model, player):
        super().__init__()

        self._logger = logging.getLogger(__name__)

        self._view = view
        self._model = model
        self._player = player

        self._media = None

        inputmap.set_state(
            inputmap.PlayerState.BROWSING,
            [
                self._view.cursor_up,
                self._view.cursor_dwn,
                self._select,
                self._go_back
            ])

        inputmap.set_state(
            inputmap.PlayerState.PLAYING,
            [
                self._stop_playing,
                self._player.volume_dwn,
                self._player.play,
                self._player.volume_up
            ])

        inputmap.map_buttons(inputmap.PlayerState.BROWSING)

        menu = self._model.list_files()
        self._view.update_menu(menu)
        self._view.display_menu()

    def on_receive(self, message):
        self._logger.debug('received message: %s', message)

        if self._media:
            self._playback()
        else:
            self._player.stop()

    def _playback(self):
        track = self._media.name.pop()

        self._view.display_track(self._media.path, track)
        self._player.run(self._media.path + track)

    def _select(self):
        self._media = self._model.get_next(self._view.cursor)
        self._logger.debug('path: %s, file: %s', self._media.path, self._media.name)

        if self._media.isdir:
            menu = self._model.list_files()

            self._view.update_menu(menu)
            self._view.display_menu()
        else:
            self._playback()

            inputmap.map_buttons(inputmap.PlayerState.PLAYING)

    def _go_back(self):
        self._model.get_previous()
        menu = self._model.list_files()

        self._view.update_menu(menu)
        self._view.display_menu()

    def _stop_playing(self):
        self._player.stop()
        self._view.display_menu()

        inputmap.map_buttons(inputmap.PlayerState.BROWSING)
