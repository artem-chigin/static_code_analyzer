import os
from enum import Enum


class Errors(Enum):
    LINE_LONGER_THAN_79 = "S001"


path_to_dir = r"C:\Users\work\Documents\JetBrains\projects\static_code_analyzer\files_to_analise"
file_name = "test_file.py"

path = os.path.join(path_to_dir, file_name)


class LongerThat79(Exception):
    pass


def longer_than_79(line_value, line_count):
    assert len(line_value) <= 79, f"Line {line_count}: {Errors.LINE_LONGER_THAN_79.value} The line is too long"


with open(path, "rt", encoding="utf-8") as file:
    line_count = 1
    for line in file:
        try:
            longer_than_79(line, line_count)
        except AssertionError as err:
            print(err)
        line_count += 1
