# Pygnore

## What is it?

**Pygnore** is a Python library for managing custom ignore patterns for files and directories, similar to `.gitignore` or `.dockerignore`.

It provides a flexible way to configure ignore rules for any project structure by using a custom protocol file (e.g., `.pygnore`) to determine which files and directories should be ignored. The system supports features like:
* Nested directories with inherited rules.
* Pattern negation using `!`.
* Wildcard matching for patterns (`*`, `?`, `**`, `[abc]`, etc.).

This functionality closely resembles the behavior of `.gitignore` and `.dockerignore`, making it intuitive for developers familiar with those systems.

## What is it for?

It helps avoid handling files or directories that are essential for the project but unnecessary for releases, archives, or other operations.

## Syntax

As mentioned above the `.pygnore` rule files are similar to the well-known `.dockerignore` or `.gitignore` files, with some minore differences. Like these systems, rules are defined by specifying paths to files and directories in `.pygnore` files, which can be placed at any nesting level.

In `.pygnore` rules, all patterns are **relative to the location of the `.pygnore` file** itself. This is the primary difference from `.gitignore`, but functions exactly like `.dockerignore`. The directories and their subdirectories (including files) are referred to as the context of the rule.

### Key Differences and Behavior

* **Context Awareness**:

    If a rule matches a file or directory (e.g., `foo`) at the top level, it applies only within the context (nesting level) of the `.pygnore` file. Patterns can also explicitly define deeper levels, e.g., `foo/bar` will match bar inside a directory named foo within the current context.

* **No Leading Slash (`/`) Anchoring**:

    Unlike `.gitignore`, `.pygnore` does not use leading slashes to anchor patterns to the root. Patterns like `/foo` or `/bar/` are treated identically to `foo` or `bar/`.

* **Trailing Slash (`/`) for Directories**:

    A trailing slash (`/`) specifically matches directories only. For example:

    - `foo/` matches a directory named `foo` but does not match `foo/bar`.
    - `foo` matches both a file or directory named `foo`.

* **Non-Greedy Directory Matching**:

    Directory matches are *non-greedy*, meaning they do not extend to the content of the directory unless explicitly specified. For instance:

    - `foo/` matches only the foo directory.
    - `foo/**` matches `foo` and all its contents.

### Wildcards (globbing patterns)

Standard wildcards, also known as globbing patterns, are used for working with multiple files. Globbing is the process of expanding a wildcard pattern into a list of pathnames that match it. A string qualifies as a wildcard pattern if it includes any of the characters `?`, `*`, or `[`.

- A hash (`#`) signifies a comment. Lines starting with `#` are ignored.
    ```
    # This is just a comment.
    ```
- A backslash (`\`) is used as an escape character to treat a special character literally.
    ```
    # The pattern below will match a file named "#.txt"
    \#.txt
    ```
- An asterisk (`*`) matches zero or more characters of any kind, excluding a slash (`/`).
    ```
    # This pattern would match "`foobar`", "`foooobar`", and anything that
    # starts with `foo` also including "`foo`" itself.
    foo*
    ```
- An exclamation mark (`!`) indicates an exception. It is used to exclude specific files or directories from being matched by previous patterns.
    ```
    # This ruleset matches all files ending with `.txt` but excludes
    # `important.txt` from the match.
    *.txt
    !important.txt
    ```
- A question mark (`?`) matches exactly one character, excluding a slash (`/`).
    ```
    # This pattern matches `hda`, `hdb`, `hdc`, and any other one-character
    # variation, excluding slashes (`/`).
    hd?
    ```
- A double asterisk (`**`) matches zero or more files and directories, including their contents, recursively.
    ```
    # This will match all `.txt` files in any directory or subdirectory.
    **/*.txt
    ```
- Square brackets (`[]`) specify a set or range of characters with an logical `OR` relationship, where any character within the brackets can match. Standard ranges include [0-9], [a-z], and [A-Z]. You can define subsets like `[0-4]` or `[a-d]`, combine ranges (e.g., `[0-9a-f]`), or mix ranges and individual characters (e.g., `[024abcXYZ]`).
    ```
    # The next pattern matches `mam`, `mum`, or `mom`.
    m[aou]m

    # The next pattern matches `mam`, `mbm`, `mcm`, or `mdm`.
    m[a-d]m
    ```
- `[!]` works as a logical `NOT`, inverting the character set specified in square brackets (`[]`). Unlike `[]`, which matches any character listed inside, `[!]` matches any character not listed between the brackets.
    ```
    # The following pattern will match files starting with `file` that are
    # followed by characters other than digits (e.g., `files`, `fileA`), but
    # it will exclude files like `file0`, `file4` (those with digits `0-9`).
    file[!0-9]
    ```

### Rule explanation

| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pattern&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example&nbsp;matches&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Explanation |
| ---- | --------------- | ----------- |
| `file0.txt` | ~~`dirA/file0.txt`~~<br />~~`dirA/dirA/file0.txt`~~<br />`file0.txt` | The simplest pattern to match files and directories located at the top level of the context. |
| `dirA/` | `dirA/`<br />~~`dirA/file0.txt`~~<br />~~`dirB/dirA/`~~ | A trailing slash (`/`) indicates that patterns match directories only. Note that directories are matched in a *non-greedy* manner, excluding their contents. |
| `dirA/file0.txt`<br /> | `dirA/file0.txt`<br />~~`dirA/dirA/file0.txt`~~<br />~~`dirB/dirA/file0.txt`~~ | All patterns are anchored to the context level, matching the specified file path relative to it. |
| `*` | `dirA/`<br />~~`dirA/file0.txt`~~<br />`file0.txt` | A positive match for any file or directory located at the root level of the context. |
| `*/` | `dirA/`<br />~~`dirA/file0.txt`~~<br />~~`file0.txt`~~ | A positive match for any directory located at the root level of the context, without including its contents. |
| `*`<br>`!*/` | ~~`dirA/`~~<br />`file0.txt` | A trick to positively match all files at the root level of the context while excluding directories. |
| `*/*` | `dirA/dirA`<br />`dirA/file0.txt` | A positive match for any second-level objects. |
| `*/file0.txt` | `dirA/file0.txt`<br />~~`dirA/dirB/file0.txt`~~<br />`dirB/file0.txt`<br />~~`file0.txt`~~ | A more material case of the previous pattern. |
| `*/*/` | `dirA/dirA/`<br />`dirA/dirB/`<br />~~`dirA/file0.txt`~~ | A positive match for any second-level directory. |
| `foo/*` | ~~`foo/`~~<br />`foo/foo/`<br />`foo/bar` | A pattern to positively match any object located directly inside the `foo` directory, excluding the `foo` directory itself. |
| `*/dirA/` | ~~`dirA/`~~<br />`dirA/dirB/`<br />~~`dirA/file0.txt`~~<br />~~`dirB/`~~<br />`dirB/dirA/` | A more material case of the previous pattern. |
| `foo*` | `foo`<br />`foobar`<br />`foooobar`<br />`foo.bar` | A positive match for any file or directory started with `foo` (at the related context level, of course). |
| `*bar` | `foobar`<br />`foooobar`<br />`foo.bar`<br />`bar` | A positive match for any file or directory ending with `bar` (again, at the related context level). |
| `**` | `dirA/`<br />`dirA/dirA/`<br />`dirA/dirA/file0.log`<br />`dirA/file0.txt`<br />`file0.txt` | A positive match for all files and directories, including their contents, recursively.|
| `**/` | `dirA/`<br />`dirA/dirA/`<br />~~`dirA/dirA/file0.log`~~<br />~~`dirA/file0.txt`~~<br />~~`file0.txt`~~ | A positive match for all directories and their subdirectories, recursively. |
| `**`<br />`!**/` | ~~`dirA/`~~<br />~~`dirA/dirA/`~~<br />`dirA/dirA/file0.log`<br />`dirA/file0.txt`<br />`file0.txt` | A trick to positively match all files, recursively while excluding directories. |
| `**/**` | ~~`dirA/`~~<br />`dirA/dirA/`<br />`dirA/dirA/file0.log`<br />`dirA/file0.txt`<br />~~`file0.txt`~~ | A recursive match for all objects located at the second level and deeper. |
| `**/**/` | ~~`dirA/`~~<br />`dirA/dirA/`<br />~~`dirA/dirA/file0.log`~~<br />~~`dirA/file0.txt`~~<br />~~`file0.txt`~~ | A recursive match for all directories located at the second level and deeper. |
| `dirA/**` | ~~`dirA/`~~<br />`dirA/dirB/`<br />`dirA/dirB/.../file0.txt` | A pattern to positively match any object inside the `dirA` directory, at any nesting level, recursively, excluding the `dirA` directory itself. |
| `dirA/**/file0.txt` | `dirA/dirA/file0.txt`<br />`dirA/dirA/dirA/file0.txt`<br />~~`dirA/file0.txt`~~ | The pattern will not match `dirA/file0.txt` because `/**/` requires at least one additional level of nesting between `dirA` and `file0.txt`. |
| `dirA/**file0.txt` | `dirA/dirA/file0.txt`<br />`dirA/dirA/dirA/file0.txt`<br />`dirA/file0.txt` | In contrast, the pattern matches `dirA/file0.txt` here, as `/**` allows matching files at any depth within `dirA`, including directly inside it. The slashes make the difference! |
| `foo**bar` | `foo/foo/bar`<br />`foo/bar/`<br />`foobar`<br /><br />`foo/foobar/`<br />`foo.bar` |  A pattern to recursively match any path starting with `foo` and ending with `bar`, regardless of nesting. |
| `foo?.bar` | `foo0.bar`<br />`foo1.bar`<br />`fooA.bar`<br />`foo..bar` | A positive match for filename where the `?` represents exactly one character other than a slash (`/`). |
| `foo?.bar` | ~~`foo.bar`~~ | Because *the `?` represents exactly one character*. |
| `foo?bar` | `foo_bar`<br />`foo.bar`<br />~~`foo/bar`~~ |  Because *other than a slash `/`*. |
| `file[0-9].txt` | `file0.txt`<br />`file1.txt`<br />...<br />`file9.txt`<br />~~`files.txt`~~ | Matches any file with the name pattern `file?.txt` where the `?` is a digit from `0` to `9`. |
| `file[!9a].txt` | `file0.txt`<br />`file1.txt`<br />...<br />~~`file9.txt`~~<br />~~`filea.txt`~~<br />`files.txt` | Matches any file with the name pattern `file?.txt` where the `?` is any character except `9`. |
| `file\*\*.txt` | `file**.txt`<br />~~`file1.txt`~~<br /> | Backslashes `\` escape the asterisks `*`, so it will handle them literally as any other characters. This means it will match a file named `file**.txt`, not any file pattern. |
| `\!file.txt`<br />`\#file.txt` | `!file.txt`<br />`\#file.txt` | Escaped exclamation mark `!` and hash sign `#` will also be handled literally as any other characters, meaning the pattern will match files named `!file.txt` and `#file.txt` without treating them as special symbols. |

## Installation
```
git clone https://github.com/fpvcode/pygnore.git
cd pygnore
```
No additional dependencies are required.

## Usage

### Basic Setup
1. Create a `.pygnore` file in your project root or specific directories.
2. Add ignore patterns to the `.pygnore` file (one per line).

Example `.pygnore` file:
```
# Ignore all `.log` files
*.log

# Ignore `temp/` directory
temp/

# Do not ignore `temp/keep.txt`
!temp/keep.txt
```

3. Use the Pygnore class to scan and check ignored files.
Example Code:
```
from pygnore import Pygnore

# Initialize Pygnore with the root directory
pygnore = Pygnore(root='path_to_your_project', protocol='.pygnore', debug=True)

# Check if a specific file or directory is ignored
print(pygnore.is_ignored('path_to_your_project/temp/some_file.log'))  # Output: True
print(pygnore.is_ignored('path_to_your_project/temp/keep.txt'))  # Output: False

# Retrieve rules for a specific directory
rules = pygnore.get_rules('path_to_your_project/temp')
for rule in rules:
    print(rule.get_pattern)
```

## Debugging

Enable the debug flag when initializing the Pygnore object to get detailed output of rule processing:
```
pygnore = Pygnore(root='path_to_your_project', debug=True)
```

## Contributing

Feel free to contribute by submitting issues or pull requests!
