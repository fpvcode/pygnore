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
    create_structure(path=tmp_path, dir_number=3, file_number=2, depth=3)

    if 1:  # Test 1.
        (tmp_path / '.pygnore').write_text('file0.txt')
        (tmp_path / 'dirA/.pygnore').write_text('!file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='1')

        (tmp_path / 'dirA/.pygnore').write_text('')

    if 1:  # Test 2.
        (tmp_path / '.pygnore').write_text('!file0.txt\n!file1.log')
        (tmp_path / 'dirA/dirA/.pygnore').write_text('file0.txt')
        (tmp_path / 'dirB/dirB/.pygnore').write_text('file1.log')

    if 1:  # Test 3.
        (tmp_path / '.pygnore').write_text('*\n!file*.*')

        test_cases = {
            'dirA': True,
            'dirB': True,
            'file0.txt': False,
            'file0.log': False,
        }

        run_test(tmp_path, test_cases, test_name='3')

        (tmp_path / 'dirA/dirB/.pygnore').write_text('')

    if 1:  # Test 4.
        (tmp_path / '.pygnore').write_text('**')
        (tmp_path / 'dirA/dirA/.pygnore').write_text('!**')

        test_cases = {
            'dirA': True,
            'dirA/dirA': True,
            'dirA/dirA/dirA': False,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': True,
            'file0.log': True,
        }

        run_test(tmp_path, test_cases, test_name='4')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
