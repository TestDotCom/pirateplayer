import logging
from signal import pause

import miniaudio
from alsaaudio import Mixer
from gpiozero import Button

from display import display_clear, display_track

logger = logging.getLogger('player')
logger.setLevel(logging.DEBUG)

m = Mixer()

volume = 5
isplaying = False


def handle_play():
    global isplaying
    isplaying = not isplaying

    stream = miniaudio.stream_file('samples/ShortCircuit.flac')
    device = miniaudio.PlaybackDevice()

    if isplaying:
        display_track('samples/', 'Short Circuit')
        device.start(stream)
    else:
        device.close()
        display_clear()

    logging.debug(f'isplaying: {isplaying}')


def volume_up():
    global volume

    if volume < 100:
        volume += 5

    m.setvolume(volume)
    logging.debug(f'volume: {m.getvolume()}')


def volume_dwn():
    global volume

    if volume > 0:
        volume -= 5

    m.setvolume(volume)
    logging.debug(f'volume: {m.getvolume()}')


def go_home():
    pass


def main():
    try:
        m.setvolume(5)

        btn_a = Button(5)
        btn_b = Button(6)
        btn_x = Button(16)
        btn_y = Button(20)

        btn_b.when_pressed = volume_dwn
        btn_y.when_pressed = volume_up
        btn_a.when_pressed = go_home
        btn_x.when_pressed = handle_play

        pause()
    except KeyboardInterrupt:
        print("\nclosing\n")
        display_clear()
