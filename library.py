from collections import defaultdict, namedtuple
import logging
import os

Media = namedtuple('Media', ['path', 'name', 'isdir'])


class Library:
    """Index current music selection."""

    def __init__(self, root):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        self._dirpath = list()
        self._dirpath.append(root + '/')

        self._filetree = defaultdict()

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3', 'm3u', 'm3u8')

        for dirpath, dirnames, filenames in os.walk(root):
            dirpath += '/'
            dirnames = list(dn + '/' for dn in sorted(dirnames))
            filenames = list(fn for fn in sorted(
                filenames) if fn.endswith(ext))

            self._filetree[dirpath] = dirnames + filenames

    def list_files(self):
        """Retrieve {current dir} available files"""
        abspath = ''.join(self._dirpath)
        return self._filetree[abspath]

    def get_next(self, index):
        """Retrive actual file selection.
        If its a dir, move inside;
        else returns a 'Media' namedtuple.
        """
        filename = self.list_files()[index]
        filepath = ''.join(self._dirpath)
        abspath = filepath + filename

        self._LOGGER.debug(
            'filename = %s, filepath = %s, abspath = %s',
            filename,
            filepath,
            abspath)

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
