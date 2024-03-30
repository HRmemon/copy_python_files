# Clipboard Code Copy Tool

## Overview

This tool is designed to facilitate the copying of code snippets from multiple files, particularly for debugging or explaining purposes. It allows users to specify a source directory and apply filters to include or exclude files based on their extensions or directories. Additionally, users can choose to modify Python files to selectively omit content, enhancing the efficiency of code copying.

## Features

- **Selective Copying**: Users can specify source directory paths and apply filters to include or exclude files based on their extensions or directories.
- **Python Code Modification**: The tool supports modifying Python files to selectively omit content, making it easier to copy only relevant code snippets.
- **Multiline Import Handling**: Handles multiline imports gracefully, ensuring complete import statements are captured correctly.
- **Logger Statement Handling**: Handles logger statements, ensuring that the code within logger statements is preserved during copying.
- **Exception Handling**: Automatically handles exception blocks by replacing them with placeholders for brevity.
- **Docstring Management**: Ensures that docstrings are associated only with definitions, improving the clarity of copied code.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/HRmemon/copy_python_files.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd copy_python_files
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To copy files' contents to the clipboard, simply execute the script with the desired source directory path:

```bash
python clipboard_copy.py /path/to/source/directory
```

### Additional Options

The tool supports several optional arguments to customize the copying process:

- `--include_ext`: Specify extensions to include.
- `--exclude_ext`: Specify extensions to exclude.
- `--include_dirs`: Specify directories to include.
- `--exclude_dirs`: Specify directories to exclude.
- `--modify_python`: Modify Python files to selectively omit content.

Example usage with optional arguments:

```bash
python clipboard_copy.py /path/to/source/directory --include_ext .py --exclude_dirs tests --modify_python
```

### Help

For more information on the available options, use the `--help` flag:

```bash
python clipboard_copy.py --help
```

## Testing

To run the tests for this tool, execute the following command:

```bash
python -m unittest copy_file_test.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This tool utilizes the following open-source libraries:

- [Pyperclip](https://pypi.org/project/pyperclip/) - For accessing the clipboard functionality.
- [argparse](https://docs.python.org/3/library/argparse.html) - For parsing command-line arguments.
