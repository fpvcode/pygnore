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
    create_structure(path=tmp_path, dir_number=3, file_number=1, depth=3)

    if 1:  # Test 1: A test for a rule sequence via negation.
        (tmp_path / '.pygnore').write_text('**')
        (tmp_path / 'dirA/.pygnore').write_text('!**/*.log')
        (tmp_path / 'dirA/dirA/.pygnore').write_text('!.pygnore')
        (tmp_path / 'dirA/dirA/dirA/.pygnore').write_text('*.log')
        (tmp_path / 'dirA/dirB/.pygnore').write_text('!.pygnore')
        (tmp_path / 'dirB/.pygnore').write_text('!*')
        (tmp_path / 'dirB/dirB/.pygnore').write_text('!.pygnore')
        (tmp_path / 'dirB/dirB/dirB/.pygnore').write_text('!*.txt')
        (tmp_path / 'dirC/.pygnore').write_text('*.*')
        (tmp_path / 'dirC/dirC/.pygnore').write_text('!*.*')
        (tmp_path / 'dirC/dirC/dirC/.pygnore').write_text('*.*')

        test_cases = {
            'dirA': True,
            'dirA/file0.log': True,
            'dirA/file0.txt': True,
            'dirA/dirA/.pygnore': False,
            'dirA/dirA/file0.log': False,
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.log': True,
            'dirA/dirB/file0.log': False,
            'dirA/dirB/file0.txt': True,
            'dirB': True,
            'dirB/dirA/file0.txt': True,
            'dirB/dirB/dirB/file0.txt': False,
            'dirB/dirB/file0.txt': True,
            'dirB/dirB/.pygnore': False,
            'dirB/file0.txt': False,
            'dirC/dirC/file0.txt': False,
            'dirC/dirC/dirC/file0.txt': True,
            'dirC/.pygnore': True,
            'dirC/file0.txt': True,
            'file0.log': True,
            'file0.txt': True,
        }

        run_test(tmp_path, test_cases, test_name='4')


# This allows running the test directly
if __name__ == '__main__':
    pytest.main()
