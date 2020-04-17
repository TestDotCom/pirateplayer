from collections import defaultdict, namedtuple
import logging
import os

Media = namedtuple('Media', ['path', 'name'])


class Library:

    def __init__(self, root):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        self._dirpath = list()
        self._dirpath.append(root + '/')

        self._filetree = defaultdict()

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3')

        for dirpath, dirnames, filenames in os.walk(root):
            dirpath += '/'
            dirnames = list(dn + '/' for dn in sorted(dirnames))
            filenames = list(fn for fn in sorted(filenames))

            self._filetree[dirpath] = dirnames + filenames

    def list_files(self):
        abspath = ''.join(self._dirpath)
        return self._filetree[abspath]

    def get_next(self, index):
        filename = self.list_files()[index]
        filepath = ''.join(self._dirpath)
        abspath = filepath + filename

        self._LOGGER.debug('filename = %s, filepath = %s, abspath = %s', filename, filepath, abspath)

        media = None

        if os.path.isfile(abspath):
            media = Media(path=filepath, name=filename)
        else:
            self._dirpath.append(filename)

        return media

    def get_previous(self):
        # don't go further than root dir
        if len(self._dirpath) > 1:
            self._dirpath.pop()
