from aaaas import image
from os import path
from unittest import TestCase

class ImageTests(TestCase):

    def test_pixel_to_char_low(self):
        self.assertEqual('#', image.to_char(0))

    def test_pixel_to_char_high(self):
        self.assertEqual(' ', image.to_char(255))

    def test_pixel_to_char_low_inverted(self):
        self.assertEqual(' ', image.to_char(0, invert=True))

    def test_pixel_to_char_high_inverted(self):
        self.assertEqual('#', image.to_char(255, invert=True))

    def test_pixel_to_char_invalid(self):
        self.assertRaises(IndexError, lambda: image.to_char(256))

    def test_image_to_ascii_max_char_width(self):
        text = image.to_ascii(path.join(path.dirname(__file__), 'test.png'),
                              max_char_width=20)
        self.assertEqual(text.index('\n'), 20)
