# pylint: disable=missing-module-docstring
from collections import namedtuple
import logging
import os

Media = namedtuple('Media', ['path', 'names', 'isdir'])


class Library():
    """Component responsible for 
    indexing every audio file supported.
    """

    def __init__(self, root: str):
        self._logger = logging.getLogger(__name__)

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3', 'm3u', 'm3u8')

        self._dirpath = list()
        self._dirpath.append(root + '/')

        self._filetree = {}

        for dirpath, dirnames, filenames in os.walk(root):
            dirpath += '/'

            # prevent string unpacking if tuple has 
            # only one element
            if type(dirnames) is str:
                dirnames = (dirnames,)
            if type(filenames) is str:
                filenames = (filenames,)
            
            dirnames = sorted(dn + '/' for dn in (dirnames))
            filenames = sorted(fn for fn in (filenames) if fn.endswith(ext))

            self._filetree[dirpath] = dirnames + filenames

    def list_files(self) -> list:
        """Retrieve current-directory available files.
        Current-directory is given by concatenating each element of _dirpath.
        """
        abspath = ''.join(self._dirpath)
        return self._filetree[abspath]

    def retrieve_file(self, index: int) -> namedtuple:
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
                playlist = sorted((track.strip()
                                   for track in p.readlines()), reverse=True)
        else:
            playlist = [filename]

        media = Media(path=filepath, names=playlist, isdir=isdir)

        return media

    def browse_up(self):
        """Return to parent folder,
        but no further than music-root.
        """
        if len(self._dirpath) > 1:
            self._dirpath.pop()
