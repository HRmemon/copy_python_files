import argparse
import os
import pyperclip
from pathlib import Path


def process_content(content, modify_python):
    if not modify_python or not content.strip():
        return content

    new_content = []
    skip_block_indent = -1
    imports_found = False
    is_multiline_import = False
    in_docstring = False
    in_definition_docstring = False
    parenthesis_balance = 0
    in_logger_statement = False
    definition_pattern = False

    for line in content.split('\n'):
        if not line.strip():
            continue

        if line.startswith("from") or line.startswith("import"):
            if not imports_found:
                new_content.append("# Imports omitted for brevity...")
            imports_found = True
            if '(' in line and ')' not in line:
                is_multiline_import = True
            continue

        if is_multiline_import:
            if ')' in line:
                is_multiline_import = False
            continue

        if line.lstrip().startswith(('def ', 'class ')):
            definition_pattern = True

        if definition_pattern and '"""' in line:
            quote_count = line.count('"""')
            if quote_count % 2 != 0:
                in_docstring = not in_docstring
                if in_docstring and definition_pattern:
                    in_definition_docstring = True
                if not in_docstring:
                    definition_pattern = False
                    if in_definition_docstring:
                        in_definition_docstring = False
                        continue 
                else: 
                    continue
            elif in_definition_docstring:
                continue

        elif in_docstring and in_definition_docstring:
            continue  # Skip lines within a definition docstring

        if line.lstrip().startswith('except '):
            skip_block_indent = len(line) - len(line.lstrip())
            new_content.append(line)
            new_content.append(f'{" " * skip_block_indent}# Code omitted for brevity...')
            new_content.append(f'{" " * (skip_block_indent + 1)}pass')
            continue

        if skip_block_indent != -1:
            block_indent = len(line) - len(line.lstrip())
            if block_indent > skip_block_indent:
                continue
            skip_block_indent = -1

        if not in_logger_statement and line.lstrip().startswith("logger."):
            in_logger_statement = True
            parenthesis_balance += line.count("(") - line.count(")")
            if parenthesis_balance <= 0:
                in_logger_statement = False
            continue

        if in_logger_statement:
            parenthesis_balance += line.count("(") - line.count(")")
            if parenthesis_balance <= 0:
                in_logger_statement = False
                parenthesis_balance = 0
                continue

            continue

        comment_index = line.find("#")
        if comment_index != -1:
            if not any(map(lambda q: q in line[:comment_index], ('"', "'"))):
                line = line[:comment_index].rstrip()
                if not line:
                    continue

        new_content.append(line)

    return '\n'.join(new_content)


def copy_files_to_clipboard(src, include_ext=None, exclude_ext=None, include_dirs=None, exclude_dirs=None, modify_python=False):
    clipboard_content = ""
    for root, dirs, files in os.walk(src):
        if include_dirs:
            dirs[:] = [d for d in dirs if d in include_dirs]
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = Path(root) / file
            if include_ext and not file_path.suffix in include_ext:
                continue
            if exclude_ext and file_path.suffix in exclude_ext:
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified_content = process_content(
                content, modify_python and file_path.suffix == '.py')

            clipboard_content += f"# File: {file_path}\n{modified_content}\n\n"

    pyperclip.copy(clipboard_content)
    print("Files copied to clipboard.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy files' contents to the clipboard with optional filtering and modification.")
    parser.add_argument("source", type=str, help="Source directory path")
    parser.add_argument("--include_ext", nargs='*',
                        help="Extensions to include")
    parser.add_argument("--exclude_ext", nargs='*',
                        help="Extensions to exclude")
    parser.add_argument("--include_dirs", nargs='*',
                        help="Directories to include")
    parser.add_argument("--exclude_dirs", nargs='*',
                        help="Directories to exclude")
    parser.add_argument("--modify_python", action='store_true',
                        help="Modify Python files to selectively omit content")

    args = parser.parse_args()
    copy_files_to_clipboard(args.source, args.include_ext, args.exclude_ext,
                            args.include_dirs, args.exclude_dirs, args.modify_python)
