"""
Matching basic patterns
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
    # Create test directories and .pygnore rules
    create_structure(path=tmp_path, dir_number=1, file_number=1, depth=2)

    if 1:  # Test 1: A positive match for the `file0.txt` on its context level.

        (tmp_path / '.pygnore').write_text('file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: A leading slash (/) is redundant.
        (tmp_path / '.pygnore').write_text('/file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Matching a directory pattern.
        (tmp_path / '.pygnore').write_text('dirA/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: Checking for a trailing slashes (/) in directory matching.
        (tmp_path / '.pygnore').write_text('/dirA/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='4')

    create_structure(path=tmp_path, dir_number=1, file_number=1, depth=1)

    if 1:  # Test 5: A negative match directory pattern against a file.
        (tmp_path / '.pygnore').write_text('file0.txt/')

        test_cases = {
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='5')

    (tmp_path / 'dirA/dirA').write_text('Ooops! It is a file!')
    if 1:  # Test 6: A negative match file pattern against a directory.
        (tmp_path / '.pygnore').write_text('dirA/dirA')

        test_cases = {
            'dirA/dirA': True,
        }

        run_test(tmp_path, test_cases, test_name='6')

    if 1:  # Test 7:  A negative match a directory-kind pattern against a file.
        (tmp_path / '.pygnore').write_text('dirA/dirA/')

        test_cases = {
            'dirA/dirA': False,
        }

        run_test(tmp_path, test_cases, test_name='7')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
