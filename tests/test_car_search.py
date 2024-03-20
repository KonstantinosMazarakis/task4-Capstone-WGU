import unittest
from server  import app
from flask_app.models.car import Car

class TestCarSearch(unittest.TestCase):
    def setUp(self):
        # Set up the application for testing
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_search_by_make(self):
        # Test searching by make
        with self.app as client:
            response = client.get('/search?search_query=Toyota&type=make')
            self.assertIn('Toyota', response.data.decode())

    def test_search_by_model(self):
        # Test searching by model
        with self.app as client:
            response = client.get('/search?search_query=supra&type=model')
            self.assertIn('supra', response.data.decode())

if __name__ == '__main__':
    unittest.main()