from collections import defaultdict
import logging
import os

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

_filetree = defaultdict()


def make_index(root):
    ext = ('wav', 'flac', 'ogg', 'aac', 'mp3')

    for dirpath, dirnames, filenames in os.walk(root):            
        _filetree[dirpath] = dirnames + \
                list(file for file in filenames if file.endswith(ext))


def list_files(dirname):
    return _filetree[dirname]


def get_index(dirpath, filename):
    return _filetree[dirpath].index(filename)
