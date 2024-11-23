"""
Test to test
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
    create_structure(path=tmp_path, dir_number=1, file_number=1, depth=1)

    if 1:  # Test 1: A positive match for an escaped asterisk (*).
        (tmp_path / '.pygnore').write_text(r'\*')
        (tmp_path / '*').write_text('')

        test_cases = {
            '*': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: A positive match for an escaped double asterisk (**).
        (tmp_path / '.pygnore').write_text(r'\*\*')
        (tmp_path / '**').write_text('')

        test_cases = {
            '**': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Another positive match for an escaped double asterisk (**).
        (tmp_path / '.pygnore').write_text(r'file\*\*.txt')
        (tmp_path / 'file**.txt').write_text('')

        test_cases = {
            'file**.txt': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: One more positive match for an escaped asterisk used as a directory contents (*).
        (tmp_path / '.pygnore').write_text(r'dirA/\*/')
        os.makedirs(tmp_path / 'dirA/*', exist_ok=True)

        test_cases = {
            'dirA': False,
            'dirA/*': True,
        }

        run_test(tmp_path, test_cases, test_name='4')

    if 1:  # Test 5: A positive match for an escaped exclamation mark (!).
        (tmp_path / '.pygnore').write_text(r'\!file.txt')
        (tmp_path / '!file.txt').write_text('')

        test_cases = {
            '!file.txt': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='5')

    if 1:  # Test 6: A positive match for an escaped hash (#)
        (tmp_path / '.pygnore').write_text(r'\#file.txt')
        (tmp_path / '#file.txt').write_text('')

        test_cases = {
            '#file.txt': True,
            'file0.txt': False,
        }

        run_test(tmp_path, test_cases, test_name='6')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
