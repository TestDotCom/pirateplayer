import logging

from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789

logger = logging.getLogger('display')
logger.setLevel(logging.DEBUG)

ds = ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=80 * 1000 * 1000
)

SIZE = (ds.width, ds.height)


def _draw_cover(path):
    cover = Image.open(path + 'cover.png').convert('RGBA')
    cover = cover.resize(SIZE)
    ds.display(cover)

    return cover


def _draw_text(string, pos, background=None):
    txt = Image.new('RGBA', SIZE, (255, 255, 255, 0))
    fnt = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 16)

    d = ImageDraw.Draw(txt)
    d.text(pos, string, font=fnt, fill=(255, 0, 0, 255))

    if background is None:
        background = Image.new('RGBA', SIZE, (118, 255, 3, 1))

    out = Image.alpha_composite(background, txt)
    ds.display(out)

    return out


def display_clear():
    ds.display(Image.new('RGB', SIZE))


def display_track(path, title):
    cover = _draw_cover(path)
    _draw_text(title, (0, 0), cover)


def display_tree(media):
    pass
