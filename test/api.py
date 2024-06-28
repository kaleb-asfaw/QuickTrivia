import unittest, time, sys, os
# Add the root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import api as ape


class TestAPI(unittest.TestCase):
    def run(self, result=None):
        # Inserts a 5-second interval between each unittest to avoid 
        # bombarding API with calls
        super().run(result)
        time.sleep(5)

    def test_category_9(self):
        response = ape.get_trivia_questions(9)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results'][0]), 6)
    
    def test_category_1(self):
        response = ape.get_trivia_questions(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response_code'], 1)
        self.assertEqual(response.json()['results'], [])



if __name__ == '__main__':
    unittest.main()