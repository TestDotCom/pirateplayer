# pylint: disable=missing-module-docstring
import logging

import mutagen
from PIL import Image, ImageFont, ImageDraw
from ST7789 import ST7789

_COLOR_BG = (0, 0, 0)
_COLOR_FG = (255, 255, 255)


# pylint: disable=too-many-instance-attributes
class View():
    """MVC design pattern -> View object.
    Responsible for displaying audio tags and album cover.

    Default display specs:
        1.3" diagonal
        240x240 resolution
        ips screen
        SPI driven
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._menu = list()
        self.cursor = 0

        try:
            self._font = ImageFont.truetype(
                'src/assets/NotoSansMono-ExtraCondensedSemiBold.ttf', 20)
        except IOError as ioe:
            self._logger.debug(ioe)
            self._font = ImageFont.load_default()

        # default screen can display up to 10 rows
        self._upper = 0
        self._lower = 10

        # PirateAudio setup
        self._ds = ST7789(
            rotation=90,
            port=0,
            cs=1,
            dc=9,
            backlight=13,
            spi_speed_hz=80 * 1000 * 1000
        )

        self._size = (self._ds.width, self._ds.height)

        self._display_logo()

    def _display_logo(self):
        try:
            logo = Image.open('src/assets/logo.png')
            logo = logo.resize(self._size)

            self._ds.display(logo)
        except FileNotFoundError as fnf:
            self._logger.debug(fnf)

    def _update_edges(self):
        if self.cursor < self._upper:
            self._lower = self._upper
            self._upper -= self._lower
        elif self.cursor >= self._lower:
            self._upper = self._lower
            self._lower += self._upper

        self.display_menu()

    def display_clear(self):
        """Draw a blank state."""
        self._ds.display(Image.new('RGB', self._size))

    def display_track(self, path, media):
        """Draw album cover, then write album, title and artist.
        Place its cover.png image inside track folder.
        """
        try:
            cover = Image.open(path + 'cover.png')
            cover = cover.resize(self._size)

        except FileNotFoundError as fnf:
            self._logger.debug(fnf)
            cover = Image.new('RGB', self._size)

        draw = ImageDraw.Draw(cover)

        try:
            info = mutagen.File(path + '/' + media)

            if 'album' in info:
                album = info['album'][0]
            else:
                album = ''

            if 'title' in info:
                title = info['title'][0]
            else:
                title = media

            if 'artist' in info:
                artist = info['artist'][0]
            else:
                artist = ''

        except mutagen.MutagenError as mge:
            self._logger.debug(mge)

        finally:
            draw.text(
                (0, 0),
                album,
                font=self._font,
                fill=_COLOR_FG)

            draw.text(
                (0, self._size[0] - 48),
                title,
                font=self._font,
                fill=_COLOR_FG)

            draw.text(
                (0, self._size[0] - 24),
                artist,
                font=self._font,
                fill=_COLOR_FG)

            self._ds.display(cover)

    def update_menu(self, menu):
        """Update internal menu list, reset current screen edges."""
        self._menu = menu
        self.cursor = 0

        self._upper = 0
        self._lower = 10

    def display_menu(self):
        """Draw current menu list, row by row."""
        img = Image.new('RGB', self._size)
        draw = ImageDraw.Draw(img)

        for index, name in enumerate(self._menu[self._upper: self._lower]):
            size_x, _ = draw.textsize(name, self._font)
            offset = index % 10

            if offset == self.cursor % 10:
                draw.rectangle((0, 24 * offset, size_x, 24 *
                                (offset + 1)), fill=_COLOR_FG)
                draw.text((0, 24 * offset), name,
                          font=self._font, fill=_COLOR_BG)
            else:
                draw.text((0, 24 * offset), name,
                          font=self._font, fill=_COLOR_FG)

        self._ds.display(img)

    def cursor_up(self):
        """Draw selection cursor a row up, then check screen edges."""
        if self.cursor == 0:
            self.cursor = len(self._menu)

        self.cursor -= 1
        self._update_edges()

    def cursor_dwn(self):
        """Draw selection cursor a row down, then check screen edges."""
        self.cursor = (self.cursor + 1) % len(self._menu)
        self._update_edges()
