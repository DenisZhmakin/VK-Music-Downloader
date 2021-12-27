import unittest
from utils import get_album_description


class TestUtils(unittest.TestCase):
    def test_good_call(self):
        result = get_album_description("Skillet", "Awake")
        self.assertEqual(result['artist'], 'Skillet')
        self.assertEqual(result['title'], 'Awake')
                    
    def test_empty_string_as_params(self):
        try:
            get_album_description("", "")
        except AttributeError as e:
            self.assertEqual(type(e), AttributeError)
    
    def test_passing_only_first_argument(self):
        result = get_album_description("Valve", "")
        self.assertFalse(result)
    
    def test_passing_only_second_argument(self):
        try:
            get_album_description("", "Is Or Will Be")
        except AttributeError as e:
            self.assertEqual(type(e), AttributeError)
    
    def test_skip_first_argument(self):
        try:
            get_album_description(None, "Is Or Will Be")
        except AttributeError as e:
            self.assertEqual(type(e), AttributeError)
    
    def test_skip_second_argument(self):
        try:
            get_album_description("Valve", None)
        except AttributeError as e:
            self.assertEqual(type(e), AttributeError)
            
    def test_skip_all_argument(self):
        try:
            get_album_description(None, None)
        except AttributeError as e:
            self.assertEqual(type(e), AttributeError)
    
    def test_without_arguments(self):
        try:
            get_album_description()
        except TypeError as e:
            self.assertEqual(type(e), TypeError)