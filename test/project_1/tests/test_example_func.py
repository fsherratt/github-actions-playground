"""Example test"""
import unittest

from project_1.example_func import add


class TestClass(unittest.TestCase):
    """Test some stuff"""

    def test_add(self):
        """Test Add function"""
        self.assertEqual(add(2, 4), 6)

    def test_add_2(self):
        """Test Add function"""
        self.assertEqual(add(4, -2), 2)
