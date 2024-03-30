import unittest
from copy_files import process_content

class TestProcessContent(unittest.TestCase):

    def test_import_removal(self):
        content = """import os
import pytz
from datetime import datetime
print('Hello, World!')"""
        expected = "# Imports omitted for brevity...\nprint('Hello, World!')"
        self.assertEqual(process_content(content, True), expected)

    def test_logger_removal(self):
        content = """logger.info('Starting')
print('Hello, World!')
logger.debug('Finished')"""
        expected = "print('Hello, World!')"
        self.assertEqual(process_content(content, True), expected)

    def test_multiline_import_removal(self):
        content = """from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    batch_processor,
)"""
        expected = "# Imports omitted for brevity..."
        self.assertEqual(process_content(content, True), expected)


    def test_inline_comment_removal(self):
        content = "x = 1  # This is a comment"
        expected = "x = 1"
        self.assertEqual(process_content(content, True), expected)

    def test_standalone_comment_removal(self):
        content = """# This is a comment line 1
# This is a comment line 2
x = 1"""
        expected = "x = 1"
        self.assertEqual(process_content(content, True), expected)

    def test_function_definition(self):
        content = "def foo(bar, baz):"
        self.assertEqual(process_content(content, True), content)

    def test_class_definition(self):
        content = '''class MyClass:
    """
    This is a class docstring
    """
    def __init__(self):
        pass'''
        expected = '''class MyClass:
    def __init__(self):
        pass'''
        self.assertEqual(process_content(content, True), expected)

    def test_multiline_string_handling(self):
        content = '''message = """
This is a multiline string
"""'''
        self.assertEqual(process_content(content, True), content)

    def test_complex_code_block(self):
        content = '''def example_function():
    """
    This is a docstring
    """
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
                print(e)
    else:
        y = 2'''
        expected = '''def example_function():
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
            # Code omitted for brevity...
             pass
    else:
        y = 2'''
        self.assertEqual(process_content(content, True), expected)

    def test_variable_assignment_with_inline_comment(self):
        content = "x = 1  # This is a comment"
        expected = "x = 1"
        self.assertEqual(process_content(content, True), expected)
    
    def test_nested_structures(self):
        content = '''def example_function():
    """
    This is a docstring
    """
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
                print(e)
    else:
        y = 2'''
        expected = '''def example_function():
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
            # Code omitted for brevity...
             pass
    else:
        y = 2'''
        self.assertEqual(process_content(content, True), expected)
    
    def test_decorator_usage(self):
        content = '''@decorator
def example_function():
    """
    This is a docstring
    """
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
                print(e)
    else:
        y = 2'''
        expected = '''@decorator
def example_function():
    if condition:
        for item in items:
            try:
                x = 1
            except Exception as e:
            # Code omitted for brevity...
             pass
    else:
        y = 2'''
        self.assertEqual(process_content(content, True), expected)

    def test_list_comprehension(self):
        content = '''squared = [x ** 2 for x in range(10)]  # This is a comment'''
        expected = '''squared = [x ** 2 for x in range(10)]'''
        self.assertEqual(process_content(content, True), expected)

    def test_nested_logger_statement(self):
        content = '''def example_function():
        logger.info(
            'Starting',
            extra={
                'key': 'value'
            }
        )
        print('Hello, World!')
        logger.debug('Finished')'''
        expected = '''def example_function():
        print('Hello, World!')'''
        self.assertEqual(process_content(content, True), expected)

    def test_mixed_content(self):
        content = '''import os
import pytz
from datetime import datetime
def example_function():
    """
    This is a docstring
    """
    logger.info('Starting')
    print('Hello, World!')
    logger.debug('Finished')
# This is a comment'''
        expected = '''# Imports omitted for brevity...
def example_function():
    print('Hello, World!')'''
        self.assertEqual(process_content(content, True), expected)
        
    def test_empty_content(self):
        content = ''
        self.assertEqual(process_content(content, True), content)


    def test_string_literals(self):
        content = '''message = "This is a string"
message = 'This is another string'
message = "This is a string with a # character"
message = 'This is another string with a # character' '''
        self.assertEqual(process_content(content, True), content)

    def test_global_statement(self):
        content = '''global x
x = 1'''
        self.assertEqual(process_content(content, True), content)

    def test_nonlocal_statement(self):
        content = '''def outer():
    x = 1
    def inner():
        nonlocal x
        x = 2'''
        self.assertEqual(process_content(content, True), content)





if __name__ == '__main__':
    unittest.main()
