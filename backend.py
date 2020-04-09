import logging
from collections import namedtuple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('backend')

Audio = namedtuple('Audio', 'path, title, fmt')
