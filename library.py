from collections import defaultdict, namedtuple
import logging
import os

Media = namedtuple('Media', ['path', 'name'])


class Library:

    def __init__(self, root):
        self._LOGGER = logging.getLogger(__name__)
        self._LOGGER.setLevel(logging.DEBUG)

        self._filetree = defaultdict()
        self._current_dir = root

        ext = ('wav', 'flac', 'ogg', 'aac', 'mp3')

        for dirpath, dirnames, filenames in os.walk(self._current_dir):
            self._filetree[dirpath] = sorted(dirnames) + \
                    list(file for file in sorted(filenames) if file.endswith(ext))

    def list_files(self):
        return self._filetree[self._current_dir]

    def get_file(self, index):
        filename = self.list_files()[index]
        filepath = os.path.join(self._current_dir, filename)

        self._LOGGER.debug('selected path: %s', filepath)

        media = None

        if os.path.isfile(filepath):
            media = Media(path=self._current_dir, name=filename)
        else:
            self._current_dir = filepath

        return media
