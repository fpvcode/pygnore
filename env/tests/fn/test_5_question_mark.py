"""
Test wildcard patterns
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
    create_structure(path=tmp_path, dir_number=2, file_number=2, depth=3)

    if 1:  # Test 1: A positive match for filename where the "?" represents exactly one character excepting a slash (/).
        (tmp_path / '.pygnore').write_text('file?.txt')

        test_cases = {
            'file0.txt': True,
            'file1.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2:  A negative match because "the `?` represents exactly one character".
        (tmp_path / '.pygnore').write_text('file0?.txt')

        test_cases = {
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3:  A negative match because "other than a slash (/)"..
        (tmp_path / '.pygnore').write_text('dirA?file0.txt')

        test_cases = {
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: A positive match of multiple question marks.
        (tmp_path / '.pygnore').write_text('f???????t')

        test_cases = {
            'file0.txt': True,
            'file1.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='4')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
