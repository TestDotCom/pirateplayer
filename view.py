import logging

from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789


class View:

    def __init__(self, filenames):
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)

        self._filenames = filenames
        self._len = len(filenames)

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
            cover = Image.open(path + 'cover.png')
            cover = cover.resize(self._size)

            font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 16)

            draw = ImageDraw.Draw(cover)
            draw.text((0, 0), title, font=font, fill=(255, 255, 255))

            self._ds.display(cover)
        except FileNotFoundError as fnf:
            self._logger.debug(fnf)
        except IOError as ioe:
            self._logger.debug(ioe)

    def display_menu(self):
        img = Image.new('RGB', self._size)
        font = ImageFont.truetype('fonts/NotoSansMono-ExtraCondensedSemiBold.ttf', 16)

        color_fg = (255, 255, 255)
        color_bg = (0, 0, 0)

        draw = ImageDraw.Draw(img)

        for index, name in enumerate(self._filenames):
            size_x, size_y = draw.textsize(name, font)

            if index == self.cursor:
                draw.rectangle((0, size_y * index, size_x, size_y * (index + 1)), fill=color_fg)
                draw.text((0, size_y * index), name, font=font, fill=color_bg)
            else:
                draw.text((0, size_y * index), name, font=font, fill=color_fg)

        self._ds.display(img)

    def cursor_up(self):
        if self.cursor == 0:
            self.cursor = self._len
        self.cursor -= 1

        self.display_menu()

    def cursor_dwn(self):
        self.cursor = (self.cursor + 1) % self._len
        self.display_menu()
