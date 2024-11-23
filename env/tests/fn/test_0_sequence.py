"""
Checking the hierarchical consistency of the rules
"""

import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from bin.pygnore import Pygnore
from common.create_structure import create_structure


def run_test(test_path, test_cases, test_name):
    # Initialize the Pygnore object
    pygnore = Pygnore(root=test_path, debug=(not 'pytest' in sys.argv[0]))

    for input, expected in test_cases.items():
        output = pygnore.is_ignored(test_path / input)
        assert output == expected, f"Test {test_name} failed for '{input}': Expected '{expected}', got '{output}'"


def test(tmp_path):

    if 1:  # Test 1: Checking the sequence of rule application.
        create_structure(path=tmp_path, dir_number=3, file_number=1, depth=3)

        (tmp_path / 'dirA/.pygnore').write_text('file0.txt')

        test_cases = {
            'dirA/dirB/dirC/file0.txt': False,
            'dirA/dirB/file0.txt': False,
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'file0.txt': False,
            'file0.log': False,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: Checking the sequence of rule application.
        (tmp_path / 'dirA/.pygnore').write_text('/file0.txt')

        test_cases = {
            'dirA/dirB/dirC/file0.txt': False,
            'dirA/dirB/file0.txt': False,
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'file0.txt': False,
            'file0.log': False,
        }

        run_test(tmp_path, test_cases, test_name='2')
        (tmp_path / 'dirA/.pygnore').write_text('')  # clear

    if 1:  # Test 3: Checking the sequence of rule application.
        (tmp_path / 'dirA/dirA/.pygnore').write_text('file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='3')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
