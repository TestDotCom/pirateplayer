import logging

import mutagen
from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789


class View:

    def __init__(self, filenames):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        self.menu = filenames
        self.menulen = len(filenames)

        # display up to N files per screen
        self._upper = 0
        self._lower = 10

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

        self._color_bg = (0, 0, 0)
        self._color_fg = (255, 255, 255)

    def _update_edges(self):
        if self.cursor < self._upper:
            self._lower = self._upper
            self._upper -= self._lower
        elif self.cursor >= self._lower:
            self._upper = self._lower
            self._lower += self._upper

        self.display_menu()

    def display_clear(self):
        self._ds.display(Image.new('RGB', self._size))

    def display_track(self, path, media):
        try:
            cover = Image.open(path + '/' + 'cover.png')
            cover = cover.resize(self._size)

            font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 20)

            draw = ImageDraw.Draw(cover)

            info = mutagen.File(path + '/' + media)

            draw.text((0, 0), info['album'][0], font=font, fill=self._color_fg)
            draw.text((0, self._size[0] - 48), info['title'][0], font=font, fill=self._color_fg)
            draw.text((0, self._size[0] - 24), info['artist'][0], font=font, fill=self._color_fg)

            self._ds.display(cover)
        except FileNotFoundError as fnf:
            self._LOGGER.debug(fnf)
        except IOError as ioe:
            self._LOGGER.debug(ioe)

    def display_menu(self):
        img = Image.new('RGB', self._size)
        font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 20)

        draw = ImageDraw.Draw(img)

        for index, name in enumerate(self.menu[self._upper:self._lower]):
            size_x, size_y = draw.textsize(name, font)
            offset = index % 10

            if offset == self.cursor % 10:
                draw.rectangle((0, 24 * offset, size_x, 24 * (offset + 1)), fill=self._color_fg)
                draw.text((0, 24 * offset), name, font=font, fill=self._color_bg)
            else:
                draw.text((0, 24 * offset), name, font=font, fill=self._color_fg)

        self._ds.display(img)

    def cursor_up(self):
        if self.cursor == 0:
            self.cursor = self.menulen

        self.cursor -= 1
        self._update_edges()

    def cursor_dwn(self):
        self.cursor = (self.cursor + 1) % self.menulen
        self._update_edges()
