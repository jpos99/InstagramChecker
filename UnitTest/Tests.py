import unittest
from main import open_page
from unittest.TestCase.te import TestCase


class MyTestCase(unittest.TestCase):

    def test_open_page(self):
        url = "https://google.com/"
        response = open_page(url)
        self.assertEqual(response , 200)

#if __name__ == '__main__':
#    unittest.main()
