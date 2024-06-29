import unittest, time, sys, os
# Add the root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.functions as func


class TestFunctions(unittest.TestCase):
    def test_validate_username_1(self):
        self.assertEqual(func.validate_username('oJ'), "VALID")

    def test_validate_username_2(self):
        self.assertEqual(func.validate_username(''), "INVALID: SPACE" )

    def test_validate_username_3(self):
        self.assertEqual(func.validate_username('this usernameis 12 chars over'), "INVALID: LONG")
    
    def test_validate_username_4(self):
        self.assertEqual(func.validate_username('yo   asdf'), "INVALID: DOUBLE SPACE")

    def test_validate_username_5(self):
        self.assertEqual(func.validate_username('oj'), "INVALID: BANNED NAME")

    
    
    
if __name__ == '__main__':
    unittest.main()