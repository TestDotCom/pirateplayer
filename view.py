import logging

from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789


class View:

    def __init__(self, filenames):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        self.menu = filenames
        self.menulen = len(filenames)

        # display up to N files per screen
        self.upper = 0
        self.lower = 11

        self._ds = ST7789(
            rotation=90,
            port=0,
            cs=1,
            dc=9,
            backlight=13,
            spi_speed_hz=80 * 1000 * 1000
        )

        self._size = (self._ds.width, self._ds.height)
        self.cursor = 0

    def display_clear(self):
        self._ds.display(Image.new('RGB', self._size))

    def display_track(self, path, title):
        try:
            cover = Image.open(path + '/' + 'cover.png')
            cover = cover.resize(self._size)

            font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 16)

            draw = ImageDraw.Draw(cover)
            draw.text((0, 0), title, font=font, fill=(255, 255, 255))

            self._ds.display(cover)
        except FileNotFoundError as fnf:
            self._LOGGER.debug(fnf)
        except IOError as ioe:
            self._LOGGER.debug(ioe)

    def display_menu(self):
        img = Image.new('RGB', self._size)
        font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 20)

        color_fg = (255, 255, 255)
        color_bg = (0, 0, 0)

        draw = ImageDraw.Draw(img)

        for index, name in enumerate(self.menu[self.upper:self.lower]):
            size_x, size_y = draw.textsize(name, font)

            if index == self.cursor:
                draw.rectangle((0, 24 * index, size_x, 24 * (index + 1)), fill=color_fg)
                draw.text((0, 24 * index), name, font=font, fill=color_bg)
            else:
                draw.text((0, 24 * index), name, font=font, fill=color_fg)

        self._ds.display(img)

    def cursor_up(self):
        if self.cursor == 0:
            self.cursor = self.menulen
        self.cursor -= 1

        self.display_menu()

    def cursor_dwn(self):
        self.cursor = (self.cursor + 1) % self.menulen

        self.display_menu()
