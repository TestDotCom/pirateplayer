import logging

from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

_DS = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=80 * 1000 * 1000
)

_SIZE = (_DS.width, _DS.height)


def _draw_cover(path):
    cover = None

    try:
        cover = Image.open(path + 'cover.png').convert('RGBA')
        cover = cover.resize(_SIZE)
        _DS.display(cover)
    except FileNotFoundError:
        _LOGGER.debug('cover not found')

    return cover


def _draw_text(string, pos, background=None):
    out = None

    try:
        txt = Image.new('RGBA', _SIZE, (255, 255, 255, 0))
        fnt = ImageFont.truetype(
            'fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 16)

        draw = ImageDraw.Draw(txt)
        draw.text(pos, string, font=fnt, fill=(118, 255, 3, 1))

        if background is None:
            background = Image.new('RGBA', _SIZE)

        out = Image.alpha_composite(background, txt)
        _DS.display(out)
    except IOError:
        _LOGGER.debug('font not found')

    return out


def display_clear():
    _DS.display(Image.new('RGB', _SIZE))


def display_track(path, title):
    cover = _draw_cover(path)
    _draw_text(title, (0, 0), cover)


def display_menu(filenames):
    for file in filenames:
        pass
