"""
Replace three or more consecutive non-escaped asterisks (*) with two.
"""
import sys
import os
import re
import string
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def clean_pattern(pattern):
    placeholder_map = {}

    def _hidescape(match):
        placeholder = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        placeholder_map[placeholder] = match.group(0)

        return placeholder

    pattern = re.sub(r'\\(.)', _hidescape, pattern)
    pattern = re.sub(r'\*{3,}', '**', re.sub(r'\\(.)', r'\\\1', pattern))

    for placeholder, value in placeholder_map.items():
        pattern = re.sub(re.escape(placeholder), value, pattern)

    return pattern


test_cases = {
    '***foobar': '**foobar',
    'foo***bar': 'foo**bar',
    'foobar***': 'foobar**',
    '****foo****bar****': '**foo**bar**',
    '***/foo/***/bar/***': '**/foo/**/bar/**',
    'foo\***': 'foo\***',
}

for input, expected in test_cases.items():
    output = clean_pattern(input)
    assert output == expected, f"Test failed for '{input}': Expected '{expected}', got '{output}'"

print("All tests passed!")
