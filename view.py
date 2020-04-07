import logging
import os.path as osp

from PilLite import Image
from ST7789 import ST7789

logging.basicConfig(level=logging.DEBUG)

ds = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=80 * 1000 * 1000
)


def draw_cover(path):
    try:
        cover = Image.open(osp.join(path, 'cover.png'))
        cover.thumbnail((ds.width, ds.height))

        ds.display(cover)
    except IOError:
        logging.error('cover not found')
