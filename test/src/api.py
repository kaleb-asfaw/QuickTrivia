import unittest, time, sys, os
# Send the root of the directory being reference DOWN 2 LEVELS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.api as ape


class TestAPI(unittest.TestCase):
    def run(self, result=None):
        # Inserts a 5-second interval between each unittest to avoid 
        # bombarding API with calls
        super().run(result)
        time.sleep(5)

    def test_category_9(self): # testing valid category response
        response = ape.get_trivia_questions(9)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results'][0]), 6)
    
    def test_category_1(self): # testing invalid category response
        response = ape.get_trivia_questions(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response_code'], 1)
        self.assertEqual(response.json()['results'], [])

    def test_server_overload(self): # testing API call overload, expecting gracious handling
        for i in range(4): 
            response = ape.get_trivia_questions(10)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()