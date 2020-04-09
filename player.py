import logging
from collections import namedtuple
from signal import pause

import miniaudio
from alsaaudio import Mixer
from gpiozero import Button

from display import display_clear, display_track

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger('player')


def main():
    mixer = Mixer()
    volume = 5
    isplaying = False

    device = miniaudio.PlaybackDevice()
    stream = None

    btn_a = Button(5)
    btn_b = Button(6)
    btn_x = Button(16)
    btn_y = Button(20)

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

    def volume_up():
        nonlocal volume
        if volume < 100:
            volume += 5

        mixer.setvolume(volume)
        logging.debug(f'volume: {mixer.getvolume()}')

    def volume_dwn():
        nonlocal volume
        if volume > 0:
            volume -= 5

        mixer.setvolume(volume)
        logging.debug(f'volume: {mixer.getvolume()}')

    try:
        btn_a.when_pressed = go_home
        btn_x.when_pressed = handle_play
        btn_b.when_pressed = volume_dwn
        btn_y.when_pressed = volume_up

        mixer.setvolume(volume)

        Audio = namedtuple('Audio', 'path, title, fmt')
        audio = Audio('samples/', 'ShortCircuit', 'flac')

        miniaudio.stream_file(audio.path + audio.title + '.' + audio.fmt)
        display_track(audio.path, audio.title)

        pause()
    except KeyboardInterrupt:
        _logger.debug('closing')

        device.close()
        display_clear()
