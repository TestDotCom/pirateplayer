from pykka import ThreadingActor
import logging

import utils.inputmap as inputmap


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

        menu = self._model.list_files().get()
        self._view.update_menu(menu)
        self._view.display_menu()

    def _select(self):
        media = self._model.get_next(self._view.cursor.get())
        self._logger.debug('path: %s, file: %s', media.path, media.name)

        if media.isdir:
            menu = self._model.list_files().get()

            self._view.update_menu(menu)
            self._view.display_menu()
        else:
            fileuri = 'file://' + media.path + '/' + media.name

            self._view.display_track(media.path, media.name)
            self._player.run(fileuri)

            inputmap.map_buttons(inputmap.PlayerState.PLAYING)

    def _go_back(self):
        self._model.get_previous()
        menu = self._model.list_files().get()

        self._view.update_menu(menu)
        self._view.display_menu()

    def _stop_playing(self):
        self._player.stop()
        self._view.display_menu()

        inputmap.map_buttons(inputmap.PlayerState.BROWSING)
