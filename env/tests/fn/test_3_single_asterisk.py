"""
Test basic asterisk-based file patterns
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
    create_structure(path=tmp_path, dir_number=1, file_number=1, depth=2)

    if 1:  # Test 1: A positive match for any file or directory located at the root level of the context.
        (tmp_path / '.pygnore').write_text('*')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: The same as the previous test.
        (tmp_path / '.pygnore').write_text('/*')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: A positive match for any directory located at the root level of the context.
        (tmp_path / '.pygnore').write_text('*/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: A trick to positively match all files at the root level of the context while excluding directories.
        (tmp_path / '.pygnore').write_text('*\n!*/')

        test_cases = {
            'dirA': False,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='4')

    create_structure(path=tmp_path, dir_number=2, file_number=1, depth=3)

    if 1:  # Test 5: A positive match for any second-level object.
        (tmp_path / '.pygnore').write_text('*/*')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/dirA/file0.txt': False,
            'dirA/dirB': True,
            'dirA/file0.txt': True,
            'dirB': False,
            'dirB/dirA': True,
            'dirB/dirB': True,
        }

        run_test(tmp_path, test_cases, test_name='5')

    if 1:  # Test 6: A positive match for any second-level directory.
        (tmp_path / '.pygnore').write_text('*/*/')

        test_cases = {
            'dirA': False,
            'dirB': False,
            'dirA/dirA': True,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'dirA/dirB': True,
            'dirB/dirA': True,
            'dirB/dirB': True,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='6')

    if 1:  # Test 7: A pattern to match any object located at the third-level within the context.
        (tmp_path / '.pygnore').write_text('*/*/*')

        test_cases = {
            'dirA/dirA': False,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='7')

    if 1:  # Test 8: A pattern to match any third-level directory.

        (tmp_path / '.pygnore').write_text('*/*/*/')

        test_cases = {
            'dirA/dirA': False,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='8')

    if 1:  # Test 9: Match files located directly inside any first-level subdirectory of "dirA".
        create_structure(path=tmp_path, dir_number=2, file_number=1, depth=3)

        (tmp_path / '.pygnore').write_text('dirA/*/file0.txt')

        test_cases = {
            'dirA/file0.txt': False,
            'dirA/dirA/file0.txt': True,
            'dirA/dirB/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='9')

    if 1:  # Test 10: A positive match for any file or directory ending with "txt")
        (tmp_path / '.pygnore').write_text('*txt')

        test_cases = {
            'file0.txt': True,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='10')

    if 1:  # Test 11:  A positive match for any file or directory starting with "file".
        (tmp_path / '.pygnore').write_text('file*')

        test_cases = {
            'dirA/file0.txt': False,
            'dirA/file0.log': False,
            'file0.txt': True,
            'file0.log': True,
        }

        run_test(tmp_path, test_cases, test_name='11')

    if 1:  # Test 12:  A positive match for any directory starting with "dir".
        (tmp_path / '.pygnore').write_text('dir*/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='12')

    if 1:  # Test 13:  It matches any object located directly inside the `dirA` directory, excluding the `dirA` itself.
        (tmp_path / '.pygnore').write_text('dirA/*')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='13')

    if 1:  # Test 14:  It matches any dot-files.
        (tmp_path / '.pygnore').write_text('.*')

        test_cases = {
            '.pygnore': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='14')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
