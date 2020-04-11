import logging
from signal import pause

from alsaaudio import Mixer, ALSAAudioError
from miniaudio import PlaybackDevice, stream_file, MiniaudioError

#from console import Audio
from display import display_clear, display_track
from inputmap import Input

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger('player')


def main():
    volume = 5
    isplaying = False
    stream = None

    def go_home():
        pass

    def handle_play():
        nonlocal isplaying
        isplaying = not isplaying

        if isplaying:
            device.start(stream)
        else:
            device.stop()

        logging.debug('isplaying: %r', isplaying)

    def volume_dwn():
        nonlocal volume
        if volume > 0:
            volume -= 5

        mixer.setvolume(volume)
        logging.debug('volume: %r', mixer.getvolume())

    def volume_up():
        nonlocal volume
        if volume < 100:
            volume += 5

        mixer.setvolume(volume)
        logging.debug('volume: %r', mixer.getvolume())

    try:
        mixer = Mixer()
        mixer.setvolume(volume)

        device = PlaybackDevice()

        inp = Input()
        inp.map_buttons([go_home, handle_play, volume_dwn, volume_up])

        #audio = Audio('samples/', 'ShortCircuit', 'flac')
        #stream_file(audio.path + audio.title + '.' + audio.fmt)
        #display_track(audio.path, audio.title)

        pause()
    except ALSAAudioError:
        _LOGGER.debug('default mixer not found')
    except MiniaudioError:
        _LOGGER.debug('default playback device not found')
    except KeyboardInterrupt:
        _LOGGER.debug('CTRL-C signal')
    finally:
        device.close()
        display_clear()
