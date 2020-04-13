from enum import Enum
import logging

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)


class GStreamer:
    
    def __init__(self):
        Gst.init(None)

        sink = Gst.ElementFactory.make('alsasink', 'sink')
        self._player = Gst.ElementFactory.make('playbin', 'pirateplayer')
        self._player.set_property('audio-sink', sink)

        self._loop = GLib.MainLoop()

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message, self._loop)

        self._state = 'idle'
    
    def _on_message(self, bus: Gst.Bus, message: Gst.Message, loop: GLib.MainLoop):
        mtype = message.type

        if mtype == Gst.MessageType.EOS:
            _LOGGER.debug("End of stream")
            self.stop()
            loop.quit()
        elif mtype == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            _LOGGER.error(err)
            _LOGGER.debug(debug)

            self.stop()
            loop.quit()
        elif mtype == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            _LOGGER.error(err)
            _LOGGER.debug(debug)

    def run(self, uri):
        self._player.set_property('uri', uri)
        self._player.set_state(Gst.State.PLAYING)

        self._loop.run()
    
    def play(self):
        if self._state == 'pause':
            self._player.set_state(Gst.State.PLAYING)
            self._state = 'play'
        elif self._state == 'play':
            self._player.set_state(Gst.State.PAUSED)
            self._state = 'pause'
    
    def stop(self):
        self._player.set_state(Gst.State.NULL)
        self._state = 'idle'
