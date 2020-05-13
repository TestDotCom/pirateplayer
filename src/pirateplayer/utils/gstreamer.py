# pylint: disable=missing-module-docstring
import logging
from threading import Thread

from pykka import ActorRegistry
import gi
gi.require_version('Gst', '1.0')
# pylint: disable=wrong-import-position
from gi.repository import Gst, GLib


class GStreamer():
    """Audio playback via Gstreamer objects."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        Gst.init(None)
        self._mainloop = GLib.MainLoop.new(None, False)

        sink = Gst.ElementFactory.make('alsasink', 'sink')  # pirate-audio hat
        self._player = Gst.ElementFactory.make('playbin', 'player')
        self._player.set_property('audio-sink', sink)

        self._player.set_property('volume', 0.1)

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)

    # pylint: disable=unused-argument
    def _on_message(self, bus, message):
        mtype = message.type

        if mtype == Gst.MessageType.EOS:
            self._logger.debug('End of stream')

            controller_ref = ActorRegistry.get_by_class_name('Controller')
            controller_ref.tell('eos')

            self.stop()

        elif mtype == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            self._logger.error(err)
            self._logger.debug(debug)

            self.stop()

        elif mtype == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            self._logger.error(err)
            self._logger.debug(debug)

    def run(self, uri):
        """Set uri as audio source and start playback."""
        self._player.set_property('uri', uri)
        self._player.set_state(Gst.State.PLAYING)

        mainloop_t = Thread(target=self._mainloop.run)
        mainloop_t.daemon = True
        mainloop_t.start()

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
        self._mainloop.quit()

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
