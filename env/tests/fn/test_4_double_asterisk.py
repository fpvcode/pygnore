"""
Test conversion of patterns from double-asterisk-based to single-asterisk-based and similar.
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
    create_structure(path=tmp_path, dir_number=2, file_number=2, depth=4)

    if 1:  # Test 1: A positive match for any object recursively.
        (tmp_path / '.pygnore').write_text('**')

        test_cases = {
            'dirA': True,
            'dirA/dirA': True,
            'dirA/dirA/dirA': True,
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': True,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: A positive match for any directoriy recursively.
        (tmp_path / '.pygnore').write_text('**/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': True,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Positively match all files at the root level of the context while excluding directories.
        (tmp_path / '.pygnore').write_text('**\n!**/')

        test_cases = {
            'dirA': False,
            'dirA/dirA': False,
            'dirA/dirA/dirA': False,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': True,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: Match any object inside the `dirA` directory, recursively, excluding the `dirA` directory itself.
        (tmp_path / '.pygnore').write_text('dirA/**')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='4')

    if 1:  # Test 5: A pattern to recursively match any path starting with "dir" and ending with "0.txt"
        (tmp_path / '.pygnore').write_text('dir**txt')
        (tmp_path / 'dirAfoo0.txt').write_text('a file')
        os.makedirs(tmp_path / 'dirA/bar0.txt', exist_ok=True)

        test_cases = {
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/file1.txt': True,
            'dirA/dirB/file0.txt': True,
            'dirA/dirB/file1.txt': True,
            'dirA/file0.txt': True,
            'dirB/dirA/file0.txt': True,
            'dirAfoo0.txt': True,  # a file
            'dirA/bar0.txt': True,  # a directory
        }

        run_test(tmp_path, test_cases, test_name='5')

    if 1:  # Test 6: It will not match "dirA/file0.txt" because "/**/" requires at least one additional level of
        #            nesting between dirA and "file0.txt".
        (tmp_path / '.pygnore').write_text('dirA/**/file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirB/file0.txt': True,
            'dirA/file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='6')

    if 1:  # Test 7: In contrast, the pattern matches dirA/file0.txt here, as /** allows matching files at any depth
        #            within dirA, including directly inside it. The slashes make the difference!
        (tmp_path / '.pygnore').write_text('dirA/**file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirB/file0.txt': True,
            'dirA/file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='7')

    if 1:  # Test 8: A recursive match for all objects located at the second level and deeper.
        (tmp_path / '.pygnore').write_text('**/**')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='8')

    if 1:  # Test 9: A recursive match for all directories located at the second level and deeper.
        (tmp_path / '.pygnore').write_text('**/**/')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='9')

    if 1:  # Test 10: A recursive match for all objects located at the second level and deeper.
        (tmp_path / '.pygnore').write_text('**/**/**')

        test_cases = {
            'dirA': False,
            'dirA/dirA': False,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.txt': True,
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='10')

    if 1:  # Test 11: A recursive match for all directories located at the third level and deeper.
        (tmp_path / '.pygnore').write_text('**/**/**/')

        test_cases = {
            'dirA': False,
            'dirA/dirA': False,
            'dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA': True,
            'dirA/dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='11')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
