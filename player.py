import logging
from signal import pause

from alsaaudio import Mixer, ALSAAudioError
from miniaudio import PlaybackDevice, stream_file, MiniaudioError

from backend import Audio
from display import display_clear, display_track
from input import Input

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger('player')


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

        logging.debug(f'isplaying: {isplaying}')

    def volume_dwn():
        nonlocal volume
        if volume > 0:
            volume -= 5

        mixer.setvolume(volume)
        logging.debug(f'volume: {mixer.getvolume()}')

    def volume_up():
        nonlocal volume
        if volume < 100:
            volume += 5

        mixer.setvolume(volume)
        logging.debug(f'volume: {mixer.getvolume()}')

    try:
        mixer = Mixer()
        mixer.setvolume(volume)

        device = PlaybackDevice()

        inp = Input()
        inp.setup([go_home, handle_play, volume_dwn, volume_up])

        audio = Audio('samples/', 'ShortCircuit', 'flac')
        stream_file(audio.path + audio.title + '.' + audio.fmt)
        display_track(audio.path, audio.title)

        pause()
    except ALSAAudioError:
        _logger.debug('default mixer not found')
    except MiniaudioError:
        _logger.debug('default playback device not found')
    except KeyboardInterrupt:
        _logger.debug('CTRL-C signal')
    finally:
        device.close()
        display_clear()
