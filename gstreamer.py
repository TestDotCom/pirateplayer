import logging

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class GStreamer():

    def __init__(self):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        Gst.init(None)

        sink = Gst.ElementFactory.make('alsasink', 'sink')  # pirate-audio hat
        self._player = Gst.ElementFactory.make('playbin', 'player')
        self._player.set_property('audio-sink', sink)

        self._player.set_property('volume', 0.1)

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)

    def _on_message(self, bus: Gst.Bus, message: Gst.Message):
        mtype = message.type

        if mtype == Gst.MessageType.EOS:
            self._LOGGER.debug("End of stream")
            self.stop()
        elif mtype == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            self._LOGGER.error(err)
            self._LOGGER.debug(debug)

            self.stop()
        elif mtype == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            self._LOGGER.error(err)
            self._LOGGER.debug(debug)

    def run(self, uri):
        self._player.set_property('uri', uri)
        self._player.set_state(Gst.State.PLAYING)

    def play(self):
        state_change, state, pending = self._player.get_state()

        if state == Gst.State.PAUSED:
            self._player.set_state(Gst.State.PLAYING)
        elif state == Gst.State.PLAYING:
            self._player.set_state(Gst.State.PAUSED)

    def stop(self):
        self._player.set_state(Gst.State.NULL)

    def set_volume(self, level):
        self._player.set_property('volume', level)

    def get_volume(self):
        return self._player.get_property('volume')
