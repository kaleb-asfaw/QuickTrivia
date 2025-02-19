import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend')))
from frontend.app import app as flask_app 

class TestFlaskServer(unittest.TestCase):
    def setUp(self): # configures the flask application for testing setting
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = flask_app.test_client()
        self.app_context = flask_app.app_context()
        self.app_context.push()

    def test_homepage(self): # testing the home page endpoint 
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_results(self): # testing the results page endpoint
        response = self.app.get("/results")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()