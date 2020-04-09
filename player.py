import logging
from signal import pause

import miniaudio
from alsaaudio import Mixer

from backend import Audio
from display import display_clear, display_track
from input import Input

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger('player')


def main():
    mixer = Mixer()
    volume = 5
    isplaying = False

    device = miniaudio.PlaybackDevice()
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
        inp = Input()
        inp.setup([go_home, handle_play, volume_dwn, volume_up])

        mixer.setvolume(volume)

        audio = Audio('samples/', 'ShortCircuit', 'flac')
        miniaudio.stream_file(audio.path + audio.title + '.' + audio.fmt)
        display_track(audio.path, audio.title)

        pause()
    except KeyboardInterrupt:
        _logger.debug('closing')

        device.close()
        display_clear()
