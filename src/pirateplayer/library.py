# pylint: disable=missing-module-docstring
from collections import defaultdict, namedtuple
import logging
import os

import pirateplayer.utils.confparse as confparse

Media = namedtuple('Media', ['path', 'name', 'isdir'])


class Library():
    """MVC design pattern -> Model actor.
    Responsible for indexing every audio file supported.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        root = confparse.get_root()

        self._dirpath = list()
        self._dirpath.append(root + '/')

        self._filetree = defaultdict()

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3', 'm3u', 'm3u8')

        for dirpath, dirnames, filenames in os.walk(root):
            dirpath += '/'
            dirnames = sorted(dn + '/' for dn in dirnames)
            filenames = sorted(fn for fn in filenames if fn.endswith(ext))

            self._filetree[dirpath] = dirnames + filenames

    def list_files(self):
        """Retrieve {current dir} available files.
        Current dir is given by concatenating each element of _dirpath.
        """
        abspath = ''.join(self._dirpath)
        return self._filetree[abspath]

    def get_next(self, index):
        """Retrive actual file selection, then
        if its a dir, move inside.
        """
        filename = self.list_files()[index]
        filepath = ''.join(self._dirpath)
        abspath = filepath + filename

        isdir = not os.path.isfile(abspath)

        if isdir:
            self._dirpath.append(filename)

        if filename.endswith(('m3u', 'm3u8')):
            with open(abspath, 'r') as p:
                playlist = sorted((track.strip() for track in p.readlines()), reverse=True)
        else:
            playlist = [filename]

        media = Media(path=filepath, name=playlist, isdir=isdir)

        return media

    def get_previous(self):
        """Return to parent folder,
        but not further than {music root}.
        """
        if len(self._dirpath) > 1:
            self._dirpath.pop()
