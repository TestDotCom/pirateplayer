import logging

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class GStreamer():
    """Audio playback via Gstreamer objects."""

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

    def _on_message(self, message: Gst.Message):
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
        """Set uri as audio source and start playback."""
        self._player.set_property('uri', uri)
        self._player.set_state(Gst.State.PLAYING)

    def play(self):
        """Pause//resume playback."""
        _, state, _ = self._player.get_state(Gst.CLOCK_TIME_NONE)

        if state == Gst.State.PAUSED:
            self._player.set_state(Gst.State.PLAYING)
        elif state == Gst.State.PLAYING:
            self._player.set_state(Gst.State.PAUSED)

    def stop(self):
        """Stop playback."""
        self._player.set_state(Gst.State.NULL)

    def volume_up(self):
        """Increase Player volume (max 1.0)."""
        volume = self._player.get_property('volume')
        if volume < 1:
            self._player.set_property('volume', volume + 0.1)

    def volume_dwn(self):
        """Decrease Player volume (min 0.0)."""
        volume = self._player.get_property('volume')
        if volume > 0:
            self._player.set_property('volume', volume - 0.1)
