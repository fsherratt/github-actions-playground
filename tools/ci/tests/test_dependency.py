"""Test the Dependency evaluation class"""
import unittest

from testbot.dependency import ProjectModification


class TestDependency(unittest.TestCase):
    def test_project_modifications(self):
        """Pass"""
        modification = ProjectModification("../..")
