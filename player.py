# import miniaudio
import logging
from signal import pause

from alsaaudio import Mixer
from gpiozero import Button

logging.basicConfig(level=logging.DEBUG)

m = Mixer()

volume = 5
isplaying = False


def handle_play():
    global isplaying
    isplaying = not isplaying

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
    return


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
