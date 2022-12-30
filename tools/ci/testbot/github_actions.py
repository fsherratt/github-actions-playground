"""Github actions integration functions"""
import dataclasses


@dataclasses.dataclass
class TestConfig:
    type: str
    run_unit_tests: bool
    run_quality: bool


def get_project_configs():
    """Retrieve project testing configurations from file"""


def generate_test_matrix():
    """Generate a test matrix"""
