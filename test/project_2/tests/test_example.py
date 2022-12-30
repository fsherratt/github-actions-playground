"""Example test"""
import unittest


class TestClass(unittest.TestCase):
    def test_pass(self):
        """True"""

    def test_fail(self):
        """Fail"""
        self.assertTrue(False)
