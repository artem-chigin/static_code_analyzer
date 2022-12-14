from enum import Enum
import re
import ast


class Symbols(Enum):
    """Fixed characters used for code analysis."""
    EMPTY = ""
    SPACE = " "
    HASH = "#"
    TODO = "todo"
    END_OF_LINE = "\n"
    SEMICOLON = ";"
    QUOTES = "'"
    DOUBLE_QUOTES = '"'
    CLASS = "class"
    DEF = "def"
    FUNC = "function"
    ARG = "argument"
    VAR = "variable"


class Errors(Enum):
    """Error messages."""

    LINE_LONGER_THAN_79 = "S001 The line is too long"
    INDENTATION_IS_NOT_A_MULTIPLE_OF_FOUR = "S002 Indention Error"
    SEMICOLON_AFTER_A_STATEMENT = "S003 Unnecessary semicolon"
    LESS_TWO_SPACES_BEFORE_A_COMMENTS = "S004 At least two spaces required before inline comments"
    TO_DO_FOUND = "S005 Find TODO in line"
    MORE_THAN_TWO_BLANK_LINES = "S006 More than two blank lines used before this line"
    TOO_MANY_SPACES_AFTER = "S007 Too many spaces after class_or_def"
    CLASS_NAME_NOT_CAMEL_CASE = "S008 Class name 'class_name' should use CamelCase"
    FUNCTION_NAME_NOT_SNAKE_CASE = "S009 Function name 'function_name' should use snake_case"
    ARG_NAME_NOT_SNAKE_CASE = "S010 Argument name 'arg_name' should be snake_case"
    VAR_NAME_NOT_SNAKE_CASE = "S011 Variable 'var_name' should be snake_case"
    ARG_VALUE_IS_MUTABLE = "S012 Default argument value is mutable"

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
    if line_value.startswith(Symbols.SPACE.value):
        for char in line_value:
            if char == Symbols.SPACE.value:
                spaces_count += 1
            else:
                break
    if spaces_count % 4 != 0:
        return create_message(path, line_number, message)


def semicolon_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.SEMICOLON_AFTER_A_STATEMENT.value
    template1 = "[#].*;"
    template2 = "[\'\"].*;.*[\'\"]"
    semicolon_char_index = line_value.find(Symbols.SEMICOLON.value)
    if semicolon_char_index != -1:
        result1 = re.search(template1, line_value)
        result2 = re.search(template2, line_value)
        if not result1 and not result2:
            return create_message(path, line_number, message)


def spaces_before_comment_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.LESS_TWO_SPACES_BEFORE_A_COMMENTS.value
    comment_char_index = line_value.find(Symbols.HASH.value)
    # print(line_value[comment_char_index - 2: comment_char_index])
    if comment_char_index != -1 and comment_char_index != 0:
        if line_value[comment_char_index - 2: comment_char_index] != Symbols.SPACE.value * 2:
            return create_message(path, line_number, message)


def todo_check(path: str, line_value: str, line_number: int) -> Errors.MSG.value:
    message = Errors.TO_DO_FOUND.value
    comment_char_index = line_value.find(Symbols.HASH.value)
    if Symbols.TODO.value in line_value[comment_char_index:].lower():
        return create_message(path, line_number, message)


def blank_lines_check(path: str, file_content: list, line_num: int) -> Errors.MSG.value:
    message = Errors.MORE_THAN_TWO_BLANK_LINES.value
    line_number = line_num - 1
    if file_content[line_number] != Symbols.END_OF_LINE.value \
            and file_content[line_number - 1] == Symbols.END_OF_LINE.value \
            and file_content[line_number - 2] == Symbols.END_OF_LINE.value \
            and file_content[line_number - 3] == Symbols.END_OF_LINE.value:
        return create_message(path, line_num, message)


def spaces_after_name_check(path: str, line_value: str, line_num: int) -> Errors.MSG.value:
    striped_line = line_value.lstrip()
    if striped_line.startswith(Symbols.CLASS.value):
        message = Errors.TOO_MANY_SPACES_AFTER.value.replace("class_or_def", Symbols.CLASS.value)
        if striped_line[6] == Symbols.SPACE.value:
            return create_message(path, line_num, message)
    elif striped_line.startswith(Symbols.DEF.value):
        message = Errors.TOO_MANY_SPACES_AFTER.value.replace("class_or_def", Symbols.DEF.value)
        if striped_line[4] == Symbols.SPACE.value:
            return create_message(path, line_num, message)


def camel_case_check(path: str, line_value: str, line_num: int) -> Errors.MSG.value:
    if Symbols.CLASS.value in line_value:
        class_name = line_value.replace("class", Symbols.EMPTY.value).replace(":", Symbols.EMPTY.value).strip()
        message = Errors.CLASS_NAME_NOT_CAMEL_CASE.value.replace("class_name", class_name)
        # template = r"class [\s]*[A-Z][a-z]+[A-Z]?[a-z]:"
        camel_template = r"[\s][A-Z][a-z]+[A-Z]?[a-z]+"
        check = re.search(camel_template, line_value)
        if not check:
            return create_message(path, line_num, message)


def snake_case_check(path: str, line_value: str, line_num: int) -> Errors.MSG.value:
    if Symbols.DEF.value in line_value:
        def_name = line_value.replace("def", Symbols.EMPTY.value)
        def_name = def_name[: def_name.find("(")].strip()
        message = Errors.FUNCTION_NAME_NOT_SNAKE_CASE.value.replace("function_name", def_name)
        snake_template = r"[\s]_?_?([a-z]+)_?([a-z\d]*)_?_?[(]"
        snake_check = re.search(snake_template, line_value)
        if not snake_check:
            return create_message(path, line_num, message)


def new_snake_case_check(path: str, name: str, line_num: int, type_of_name: str) -> Errors.MSG.value:
    if type_of_name == Symbols.FUNC.value:
        message = Errors.FUNCTION_NAME_NOT_SNAKE_CASE.value.replace("function_name", name)
    elif type_of_name == Symbols.ARG.value:
        message = Errors.ARG_NAME_NOT_SNAKE_CASE.value.replace("arg_name", name)
    elif type_of_name == Symbols.VAR.value:
        message = Errors.VAR_NAME_NOT_SNAKE_CASE.value.replace("var_name", name)
    template = r"\b_?_?[\da-z_]+_?_?\b"
    check = re.match(template, name)
    if not check:
        return create_message(path, line_num, message)


def mutable_args_check(path: str, data, line_num: int) -> Errors.MSG.value:
    if type(data) not in {int, str, bool, tuple, frozenset} and data is not None:
        message = Errors.ARG_VALUE_IS_MUTABLE.value
        return create_message(path, line_num, message)


def code_analyze(path: str):
    with open(path, "rt", encoding="utf-8") as file:
        line_counter = 1
        path_for_a_message = path[2:]
        content = file.readlines()

        tree = ast.parse("".join(content))
        # print(ast.dump(tree))
        function_names = {}
        argument_names = {}
        node = ast.walk(tree)
        var_names = {}
        arg_types = {}

        for n in node:
            if isinstance(n, ast.FunctionDef):
                function_names[n.lineno] = n.name
                argument_names[n.lineno] = [a.arg for a in n.args.args]
                arg_types[n.lineno] = [ast.literal_eval(i) for i in n.args.defaults]
                vars = [i.targets for i in n.body if isinstance(i, ast.Assign)]
                for var_name in vars:
                    if isinstance(var_name[0], ast.Name):
                        var_names[var_name[0].lineno] = var_name[0].id

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

            result_spaces_after_name = spaces_after_name_check(path_for_a_message, line, line_counter)
            if result_spaces_after_name:
                print(result_spaces_after_name)

            result_camel_case = camel_case_check(path_for_a_message, line, line_counter)
            if result_camel_case:
                print(result_camel_case)

            # result_snake_case = snake_case_check(path_for_a_message, line, line_counter)
            # if result_snake_case:
            #     print(result_snake_case)

            if line_counter in function_names.keys():
                result_new = new_snake_case_check(path_for_a_message, function_names[line_counter], line_counter, Symbols.FUNC.value)
                if result_new:
                    print(result_new)

            if line_counter in argument_names.keys():
                for arg in argument_names[line_counter]:
                    result = new_snake_case_check(path_for_a_message, arg, line_counter, Symbols.ARG.value)
                    if result:
                        print(result)
                        break

            if line_counter in var_names.keys():
                # for name in var_names[line_counter]:
                result = new_snake_case_check(path_for_a_message, var_names[line_counter], line_counter, Symbols.VAR.value)
                if result:
                    print(result)

            if line_counter in arg_types.keys():
                for data in arg_types[line_counter]:
                    # print(data)
                    check = mutable_args_check(path_for_a_message, data, line_counter)
                    if check:
                        print(check)

            line_counter += 1
