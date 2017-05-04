from aaaas.server import app
from io import StringIO
from os import path
from unittest import TestCase

class ServerTest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(b'OK', resp.data)

    def test_post_images_without_image(self):
        resp = self.client.post('/images')
        self.assertEqual(400, resp.status_code)

    def test_post_images_with_non_image(self):
        with open(__file__, 'rb') as f:
            resp = self.client.post('/images',
                                    data={'image': (f, __file__)})
        self.assertEqual(400, resp.status_code)

    def test_post_images_with_image(self):
        with open(path.join(path.dirname(__file__), 'test.png'), 'rb') as f:
            resp = self.client.post('/images',
                                    data={'image': (f, 'test.png')})
        self.assertEqual(200, resp.status_code)

    # def test_post_images_with_huge_image(self):
    #     pass
