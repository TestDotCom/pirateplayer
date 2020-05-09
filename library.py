from collections import defaultdict, namedtuple
import logging
import os

import utils.confparse as confparse

Media = namedtuple('Media', ['path', 'name', 'isdir'])


class Library:
    """Index current music selection."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        root = confparse.get_root()

        self._dirpath = list()
        self._dirpath.append(root + '/')

        self._filetree = defaultdict()

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3')

        for dirpath, dirnames, filenames in os.walk(root):
            dirpath += '/'
            dirnames = list(dn + '/' for dn in sorted(dirnames))
            filenames = list(fn for fn in sorted(filenames) if fn.endswith(ext))

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
        media = Media(path=filepath, name=filename, isdir=isdir)

        if isdir:
            self._dirpath.append(filename)

        return media

    def get_previous(self):
        """Return to parent folder,
        but not further than {music root}.
        """
        if len(self._dirpath) > 1:
            self._dirpath.pop()
