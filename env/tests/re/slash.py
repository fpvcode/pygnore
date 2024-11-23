"""
Remove redundant slashes (/).
"""
import re


def clean_pattern(pattern):
    return (re.sub(r'/+', '/', pattern)).lstrip('/')


test_cases = {
    '/foo/bar': 'foo/bar',
    'foo/bar': 'foo/bar',
    'foo/bar/': 'foo/bar/',
    '//foo/bar/': 'foo/bar/',
    'foo//bar/': 'foo/bar/',
    'foo/bar//': 'foo/bar/',
    '///foo/bar': 'foo/bar',
    'foo///bar': 'foo/bar',
    'foo/bar///': 'foo/bar/',
    '///foo///bar///': 'foo/bar/',
}

for input, expected in test_cases.items():
    output = clean_pattern(input)
    assert output == expected, f"Test failed for '{input}': Expected '{expected}', got '{output}'"

print("All tests passed!")
