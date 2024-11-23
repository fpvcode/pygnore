import os
import glob
import shutil
import importlib.util
from pathlib import Path
import pytest

def clean_pycache(directory):
    """Remove __pycache__ directories."""

    for dirpath, dirnames, filenames in os.walk(directory):
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            shutil.rmtree(pycache_path)


def run_tests():
    """Run all tests in the tests directory."""

    env_dir = 'env'
    test_modules = []  # List to keep track of test modules

    # Clean up __pycache__ before running tests
    clean_pycache(env_dir)

    for test_file in sorted(glob.glob(os.path.join(env_dir, 'tests/fn', 'test_*.py'))):
        # Run test.py with the path to test_env as an argument
        if os.path.exists(test_file):
            spec = importlib.util.spec_from_file_location("test", test_file)
            test_module = importlib.util.module_from_spec(spec)

            # Add the loaded test module to the list
            test_modules.append(test_module)

    # After running all setup scripts, run pytest to execute all tests
    if test_modules:  # Only run pytest if there are test modules
        # pytest.main(['-q', '--tb=line', *[test.__file__ for test in test_modules]])
        pytest.main(['-s', '--tb=line', *[test.__file__ for test in test_modules]])

    # Clean up __pycache__ after running tests
    clean_pycache(env_dir)


if __name__ == '__main__':
    run_tests()
