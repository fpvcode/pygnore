"""
Module:        Pygnore
Description:   A utility for handling ignore-like patterns in a file system
Author:        Andrii Burkatskyi aka andr11b
Year:          2024
Version:       0.0.1
License:       MIT License
Email:         andr11b@ukr.net, fpvcode@gmail.com
Link:          https://github.com/fpvcode/pygnore
"""

import os
import re
import random
import string

from collections import defaultdict


class Pygnore:
    """
    A class for managing file system ignore patterns using custom `.pygnore` protocol files.

    This class scans directories starting from a root path, reads `.pygnore` files to load ignore rules,
    and determines whether files or directories should be ignored based on those rules.

    Attributes:
        _root (str): The root directory where the scanning starts.
        _debug (bool): Flag to enable debug output.
        _protocol (str): The filename of the protocol file to be processed (default: `.pygnore`).
        _rules (dict): A dictionary mapping directories to their associated rules.
        _ignored (dict): A dictionary of file paths and whether they are ignored.
    """

    class PygnoreRule:
        """
        Represents a single rule in the ignore protocol.

        Attributes:
            pattern (str): The raw pattern string from the ignore file.
            context (str): The directory context for the rule.
            regex (str): The compiled regular expression representing the rule.
            is_negation (bool): Whether the rule negates matching files.
            is_directory_only (bool): Whether the rule applies only to directories.
        """

        def __init__(self, pattern, context='', parent=None):
            if parent is None or not isinstance(parent, Pygnore):
                raise Exception("Cannot instantiate PygnoreRule directly.")

            self._rule = self._compose(pattern, context)

        def __str__(self):
            return self._rule

        def __repr__(self):
            return f'PygnoreRule({self._rule})'

        def _compose(self, pattern, context):
            placeholder_map = {}

            def _hidescape(match):
                placeholder = self._random()
                placeholder_map[placeholder] = match.group(0)

                return placeholder

            context = '' if context in {'.', '/'} else re.escape(context.rstrip('/')) + r'/'

            pattern = pattern.strip()

            repattern = re.sub(r'\\(.)', _hidescape, pattern)

            # Ignore empty lines and comments
            if repattern.strip() == '' or repattern[0] == '#':
                repattern = ''

            # Handle negation patterns (start with '!')
            if repattern.startswith('!'):
                is_negation = True
                repattern = repattern[1:]
            else:
                is_negation = False

            # Normalize slashes, e.g., `//` -> `/`, and remove leading slashes.
            repattern = (re.sub(r'/+', '/', repattern)).lstrip('/')
            #  Normalize asterisks, i.e., `***` -> `**`.
            repattern = re.sub(r'\*{3,}', '**', repattern)

            # Trailing slash (/) means this is explicitly a directory pattern
            is_directory_only = repattern.endswith('/')
            repattern = repattern.rstrip('/')

            if not is_directory_only and repattern == '**':
                repattern = r'.+$'
            elif not is_directory_only and repattern == '*':
                repattern = r'[^/]+/?$'
            else:

                def _rebrackets(match):
                    content = match.group(0)

                    if content.startswith('[!'): content = content.replace('[!', '[^')

                    placeholder = self._random()
                    placeholder_map[placeholder] = content

                    return f"{placeholder}"

                repattern = re.sub(r'\[.*?\]', _rebrackets, repattern)

                is_end_anchor = False

                if not is_directory_only:
                    instance = r'/\*\*$'  # a trailing `/**`
                    if re.search(instance, repattern):
                        is_end_anchor = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'/(.+)$'
                        repattern = re.sub(instance, placeholder, repattern)

                    instance = r'\*\*$'  # a trailing `**`
                    if re.search(instance, repattern):
                        is_end_anchor = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'.*'
                        repattern = re.sub(instance, placeholder, repattern)

                    instance = r'/\*$'  # a trailing `/*`
                    if re.search(instance, repattern):
                        is_end_anchor = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'/[^/]+/?$'
                        repattern = re.sub(instance, placeholder, repattern)

                instance = r'\*\*'  # all instances of the `**`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'(.*)?'
                    repattern = re.sub(instance, placeholder, repattern)

                instance = r'\*'  # all instances of the `*`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'[^/]*'
                    repattern = re.sub(instance, placeholder, repattern)

                instance = r'\?'  # all instances of the the `?`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'[^/]{1}'
                    repattern = re.sub(instance, placeholder, repattern)

                repattern = re.escape(repattern)

                for placeholder, value in placeholder_map.items():
                    repattern = re.sub(re.escape(placeholder), value, repattern)

                if not is_end_anchor:
                    if is_directory_only:
                        repattern += r'\/$'  # matches directory paths that explicitly end with a slash (/)
                    else:
                        repattern += r'(/?$)'  # matches paths that may or may not end with a slash (/)
            repattern = '^' + context + repattern

            return {
                'pattern': pattern,
                'context': context,
                'regex': repattern,
                'is_negation': is_negation,
                'is_directory_only': is_directory_only,
            }

        def match(self, rel_path):
            return bool(re.compile(self.get_regex).match(rel_path))

        def _random(self, k=16):
            return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

        @property
        def get_rule(self):
            return self._rule

        @property
        def get_pattern(self):
            return self._rule['pattern']

        @property
        def get_regex(self):
            return self._rule['regex']

        @property
        def get_context(self):
            return self._rule['context']

        @property
        def is_directory_only(self):
            return self._rule['is_directory_only']

        @property
        def is_negation(self):
            return self._rule['is_negation']

    def __init__(self, root, protocol='.pygnore', debug=False):
        """
        Initialize the Pygnore instance.

        Args:
            root (str): The root directory to scan.
            protocol (str): The name of the ignore protocol file.
            debug (bool): Whether to enable debug output.
        """
        self._root = os.path.normpath(os.path.abspath(root))
        self._debug = debug
        self._protocol = protocol
        self._rules = defaultdict(list)
        self._ignored = {}
        self._map_rules()
        self._map_paths()

    def _map_rules(self):
        """
        Collect all relative paths and check them against the accumulated rules.

        Traverses directories from the root to the deepest level to gather
        ignore rules from protocol files.
        """
        for dirpath, _, filenames in sorted(os.walk(self._root), key=lambda x: x[0]):
            ancestor = dirpath if dirpath == self._root else os.path.dirname(dirpath)
            self._rules[dirpath].extend(self._rules[ancestor])

            # Process local rules if the protocol file exists
            if self._protocol in filenames:
                self._parse_file(dirpath, os.path.join(dirpath, self._protocol))

        if self._debug:
            print('\n### <<< Rules ###\n')
            for path, rules in self._rules.items():
                print(f"{os.path.relpath(path, self._root)}")
                for rule in rules:
                    print(f"    {', '.join(f'{key}: {value}' for key, value in rule.get_rule.items())}")
            print('\n### >>> Rules ###\n')

    def _parse_file(self, directory, filepath):
        """
        Load rules from the file and store them in rules.

        Args:
            directory (str): The directory containing the protocol file.
            filepath (str): The full path to the protocol file.
        """
        context = os.path.relpath(directory, self._root)

        with open(filepath, 'r') as file:
            for line in file:
                pattern = line.strip()

                if pattern and not pattern.startswith('#'):
                    rule = self.PygnoreRule(pattern, parent=self, context=context)
                    self._rules[directory].append(rule)

    def _map_paths(self):
        """
        Collect all relative paths and check them against the accumulated rules.

        This method traverses the file tree and applies the rules to each file
        and directory to determine if they should be ignored.
        """
        rel_paths = []

        for dirpath, dirnames, filenames in sorted(os.walk(self._root), key=lambda x: x[0]):
            for dirname in dirnames:
                dir_rel_path = os.path.relpath(os.path.join(dirpath, dirname), self._root)
                rel_paths.append(dir_rel_path + os.sep)

            for filename in filenames:
                file_rel_path = os.path.relpath(os.path.join(dirpath, filename), self._root)
                rel_paths.append(file_rel_path)

        for rel_path in rel_paths:
            abs_path = os.path.join(self._root, rel_path)
            is_ignored = False

            # Check rules for the directory containing the file/directory
            directory = os.path.dirname(abs_path) if abs_path != self._root else self._root

            for rule in self._rules[directory]:
                if rule.match(rel_path):
                    is_ignored = not rule.is_negation

            # Store the path status in the dictionary
            self._ignored[rel_path] = is_ignored

    def is_ignored(self, path):
        """
        Public method for checking if a path is ignored.

        Args:
            path (str): The absolute or relative path to check.

        Returns:
            bool: True if the path is ignored, False otherwise.
        """
        path = os.path.normpath(os.path.abspath(path))
        path = os.path.relpath(path, self._root) + (os.sep if os.path.isdir(path) else '')

        is_ignored = self._ignored.get(path, None)

        if self._debug: print(f"'{path}': {is_ignored}")

        return is_ignored

    def get_rules(self, directory):
        """
        Public method to get rules for a specific directory.

        Args:
            directory (str): The directory to fetch rules for.

        Returns:
            list: A list of PygnoreRule objects for the directory.
        """
        return self._rules.get(directory, [])

    def add_rule(self, directory, pattern):
        """
        Optionally, add a new rule to a specific directory.

        Args:
            directory (str): The directory to add the rule to.
            pattern (str): The ignore pattern to add.
        """
        pattern = pattern.strip()
        if pattern and not pattern.startswith('#'):
            rule = self.PygnoreRule(pattern, parent=self)
            self._rules[directory].append(rule)


if __name__ == '__main__':
    pygnore = Pygnore(root='.', protocol='.pygnore', debug=False)
