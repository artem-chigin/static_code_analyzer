from enum import Enum
import re


class ImportantSymbols(Enum):
    """Fixed characters used for code analysis."""

    SPACE = " "
    HASH = "#"
    TODO = "todo"
    END_OF_LINE = "\n"
    SEMICOLON = ";"
    QUOTES = "'"
    DOUBLE_QUOTES = '"'


class Errors(Enum):
    """Error messages."""

    LINE_LONGER_THAN_79 = "S001 The line is too long"
    INDENTATION_IS_NOT_A_MULTIPLE_OF_FOUR = "S002 Indention Error"
    SEMICOLON_AFTER_A_STATEMENT = "S003 Unnecessary semicolon"
    LESS_TWO_SPACES_BEFORE_A_COMMENTS = "S004 At least two spaces required before inline comments"
    TO_DO_FOUND = "S005 Find TODO in line"
    MORE_THAN_TWO_BLANK_LINES = "S006 More than two blank lines used before this line"
    MSG = "Error message"


def create_message(path: str, line_number: int, msg: str) -> Errors.MSG.value:
    return f"{path}: Line {line_number}: {msg}"


def length_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.LINE_LONGER_THAN_79.value
    if len(line_value) > 79:
        return create_message(path, line_number, message)


def indentation_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.INDENTATION_IS_NOT_A_MULTIPLE_OF_FOUR.value
    spaces_count = 0
    if line_value.startswith(ImportantSymbols.SPACE.value):
        for char in line_value:
            if char == ImportantSymbols.SPACE.value:
                spaces_count += 1
            else:
                break
    if spaces_count % 4 != 0:
        return create_message(path, line_number, message)


def semicolon_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.SEMICOLON_AFTER_A_STATEMENT.value
    template1 = "[#].*;"
    template2 = "[\'\"].*;.*[\'\"]"
    semicolon_char_index = line_value.find(ImportantSymbols.SEMICOLON.value)
    if semicolon_char_index != -1:
        result1 = re.search(template1, line_value)
        result2 = re.search(template2, line_value)
        if not result1 and not result2:
            return create_message(path, line_number, message)


def spaces_before_comment_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.LESS_TWO_SPACES_BEFORE_A_COMMENTS.value
    comment_char_index = line_value.find(ImportantSymbols.HASH.value)
    # print(line_value[comment_char_index - 2: comment_char_index])
    if comment_char_index != -1 and comment_char_index != 0:
        if line_value[comment_char_index - 2: comment_char_index] != ImportantSymbols.SPACE.value * 2:
            return create_message(path, line_number, message)


def todo_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.TO_DO_FOUND.value
    comment_char_index = line_value.find(ImportantSymbols.HASH.value)
    if ImportantSymbols.TODO.value in line_value[comment_char_index:].lower():
        return create_message(path, line_number, message)


def blank_lines_check(path: str, file_content: list, line_num: int) -> Errors.MSG.value:
    message = Errors.MORE_THAN_TWO_BLANK_LINES.value
    line_number = line_num - 1
    if file_content[line_number] != ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 1] == ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 2] == ImportantSymbols.END_OF_LINE.value \
            and file_content[line_number - 3] == ImportantSymbols.END_OF_LINE.value:
        return create_message(path, line_num, message)


def code_analyze(path: str):
    with open(path, "rt", encoding="utf-8") as file:
        line_counter = 1
        path_for_a_message = path[2:]
        content = file.readlines()

        for line in content:
            length_check_result = length_check(path_for_a_message, line, line_counter)
            if length_check_result:
                print(length_check_result)

            result_indentation_check = indentation_check(path_for_a_message, line, line_counter)
            if result_indentation_check:
                print(result_indentation_check)

            result_semicolon_check = semicolon_check(path_for_a_message, line, line_counter)
            if result_semicolon_check:
                print(result_semicolon_check)

            result_spaces_before_comment = spaces_before_comment_check(path_for_a_message, line, line_counter)
            if result_spaces_before_comment:
                print(result_spaces_before_comment)

            result_todo_check = todo_check(path_for_a_message, line, line_counter)
            if result_todo_check:
                print(result_todo_check)

            result_blank_lines_check = blank_lines_check(path_for_a_message, content, line_counter)
            if result_blank_lines_check:
                print(result_blank_lines_check)

            line_counter += 1
