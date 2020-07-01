from unittest import TestCase
from unittest.mock import MagicMock, patch

from pirateplayer.library import Library

class TestLibrary(TestCase):

    def setUp(self):
        self._root = '~/Music'
        
        dirtree = [
            (self._root, ('Gorillaz', 'Daft Punk'), ('test.ogg')),
            ('Gorillaz', ('Song Machine', 'Plastic Beach'), ()),
            ('Song Machine', (), ('Desole.flac', 'Aries.flac')),
            ('Daft Punk', ('Discovery'), ()),
            ('Discovery', (), ('One More Time.flac'))
        ]

        self._mock_root = patch('pirateplayer.utils.confparse.get_root', return_value=self._root)
        self._mockWalk = patch('os.walk', return_value=dirtree)

    def test_init_library(self):
        expected_filetree = {
            self._root + '/' : sorted(('Gorillaz/', 'Daft Punk/', 'test.ogg')),
            'Gorillaz/' : sorted(('Song Machine/', 'Plastic Beach/')),
            'Song Machine/' : sorted(('Desole.flac', 'Aries.flac')),
            'Daft Punk/' : ['Discovery/'],
            'Discovery/' : ['One More Time.flac']
        }

        with self._mock_root:
            with self._mockWalk:
                library = Library()
                self.assertEqual(library._filetree, expected_filetree)

    def test_list_files(self):
        expected_list = sorted(('Gorillaz/', 'Daft Punk/', 'test.ogg'))

        with self._mock_root:
            with self._mockWalk:
                library = Library()
                self.assertEqual(library.list_files(), expected_list)

    def test_retrieve_file(self):
        expected_file = ['Daft Punk/']

        with self._mock_root:
            with self._mockWalk:
                library = Library()
                self.assertEqual(library.retrieve_file(0).names, expected_file)

    def test_browse_up(self):
        with self._mock_root:
            expected_path = [self._root + '/']

            with self._mockWalk:
                library = Library()

                library.retrieve_file(0)
                library.browse_up()
                self.assertEqual(library._dirpath, expected_path)
