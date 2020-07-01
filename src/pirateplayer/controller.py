# pylint: disable=missing-module-docstring
import logging

import pirateplayer.utils.inputmap as inputmap


class Controller():
    """Component responsible for 
    coordinating each other object.
    """

    def __init__(self, view, model, player, pins):
        self._logger = logging.getLogger(__name__)

        self._view = view
        self._model = model

        player.set_eos_callback(self._eos_callback)
        self._player = player

        self._media = None

        inputmap.init(pins)

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

    def _eos_callback(self):
        if self._media.names:
            self._playback()
        else:
            self._player.stop()

    def _playback(self):
        track = self._media.names.pop()
        uri = self._media.path + track

        self._logger.debug("playing: %s", uri)

        self._view.display_track(self._media.path, track)
        self._player.run(self._media.path + track)

    def _select(self):
        self._media = self._model.retrieve_file(self._view.cursor)

        if self._media.isdir:
            menu = self._model.list_files()

            self._view.update_menu(menu)
            self._view.display_menu()
        else:
            self._playback()

            inputmap.map_buttons(inputmap.PlayerState.PLAYING)

    def _go_back(self):
        self._model.browse_up()
        menu = self._model.list_files()

        self._view.update_menu(menu)
        self._view.display_menu()

    def _stop_playing(self):
        self._player.stop()
        self._view.display_menu()

        inputmap.map_buttons(inputmap.PlayerState.BROWSING)
