import os
from enum import Enum
import re


class ImportantSymbols(Enum):
    SPACE = " "
    HASH = "#"
    TODO = "todo"
    END_OF_LINE = "\n"
    SEMICOLON = ";"
    QUOTES = "'"
    DOUBLE_QUOTES = '"'


class Errors(Enum):
    LINE_LONGER_THAN_79 = "S001 The line is too long"
    INDENTATION_IS_NOT_A_MULTIPLE_OF_FOUR = "S002 Indention Error"
    SEMICOLON_AFTER_A_STATEMENT = "S003 Unnecessary semicolon"
    LESS_TWO_SPACES_BEFORE_A_COMMENTS = "S004 At least two spaces required before inline comments"
    TO_DO_FOUND = "S005 Find TODO in line"
    MORE_THAN_TWO_BLANK_LINES = "S006 More than two blank lines used before this line"


path_to_dir = r"C:\Users\work\Documents\JetBrains\projects\static_code_analyzer\files_to_analise"
file_name = "test_file.py"

path = os.path.join(path_to_dir, file_name)


class LongerThat79(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.LINE_LONGER_THAN_79.value}"
        super().__init__(self.message)


class IndentationException(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.INDENTATION_IS_NOT_A_MULTIPLE_OF_FOUR.value}"
        super().__init__(self.message)


class SemicolonError(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.SEMICOLON_AFTER_A_STATEMENT.value}"
        super().__init__(self.message)


class LessTwoSpacesError(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.LESS_TWO_SPACES_BEFORE_A_COMMENTS.value}"
        super().__init__(self.message)


class ToDoError(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.TO_DO_FOUND.value}"
        super().__init__(self.message)


class BlancLinesError(Exception):
    def __init__(self, line_count):
        self.message = f"Line {line_count}: {Errors.MORE_THAN_TWO_BLANK_LINES.value}"
        super().__init__(self.message)


def length_check(line_value, line_number):
    if len(line_value) > 79:
        raise LongerThat79(line_number)


def indentation_check(line_value, line_number):
    spaces_count = 0
    if line_value.startswith(ImportantSymbols.SPACE.value):
        for char in line_value:
            if char == " ":
                spaces_count += 1
            else:
                break
    if spaces_count % 4 != 0:
        raise IndentationException(line_number)


def semicolon_check(line_value, line_number):
    template1 = "[#].*;"
    template2 = "[\'\"].*;.*[\'\"]"
    semicolon_char_index = line_value.find(ImportantSymbols.SEMICOLON.value)
    if semicolon_char_index != -1:
        result1 = re.search(template1, line_value)
        result2 = re.search(template2, line_value)
        if not result1 and not result2:
            raise SemicolonError(line_number)


def spaces_before_comment_check(line_value, line_number):
    comment_char_index = line_value.find(ImportantSymbols.HASH.value)
    # print(line_value[comment_char_index - 2: comment_char_index])
    if comment_char_index != -1 and comment_char_index != 0:
        if line_value[comment_char_index - 2: comment_char_index] != ImportantSymbols.SPACE.value * 2:
            raise LessTwoSpacesError(line_number)


def todo_check(line_value, line_number):
    comment_char_index = line_value.find(ImportantSymbols.HASH.value)
    if ImportantSymbols.TODO.value in line_value[comment_char_index:].lower():
        raise ToDoError(line_number)


def blank_lines_check(file_content, line_num):
    line_number = line_num - 1
    if file_content[line_number] != ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 1] == ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 2] == ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 3] == ImportantSymbols.END_OF_LINE.value:
        raise BlancLinesError(line_num)


with open(path, "rt", encoding="utf-8") as file:
    line_counter = 1
    content = file.readlines()

    for line in content:
        try:
            length_check(line, line_counter)
        except LongerThat79 as err:
            print(err)

        try:
            indentation_check(line, line_counter)
        except IndentationException as err:
            print(err)

        try:
            semicolon_check(line, line_counter)
        except SemicolonError as err:
            print(err)

        try:
            spaces_before_comment_check(line, line_counter)
        except LessTwoSpacesError as err:
            print(err)

        try:
            todo_check(line, line_counter)
        except ToDoError as err:
            print(err)

        try:
            blank_lines_check(content, line_counter)
        except BlancLinesError as err:
            print(err)

        line_counter += 1
