import unittest
import sys
import os
from unittest.mock import patch, MagicMock


# Add the frontend directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.app import app as flask_app 

class TestFlaskServer(unittest.TestCase):
   
    def setUp(self):
        # Mock Firebase initialization
        with patch('firebase_admin.initialize_app'):
            from src.leaderboard import add_score, get_leaderboard

        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = flask_app.test_client()
        self.app_context = flask_app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_homepage(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the home page', response.data)
    
    def test_results(self):
        response = self.app.get("/results")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
