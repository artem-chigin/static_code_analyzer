import os
import argparse
import functions_for_analyze


parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=None)
args = parser.parse_args()

files_for_work = []

path = os.path.join(".", args.path)

if os.path.isdir(path):

    root_path = os.walk(path, topdown=False)

    for root, dirs, files in root_path:
        for name in files:
            path_to_file = os.path.join(root, name)
            if path_to_file.endswith(".py"):
                files_for_work.append(path_to_file)
elif os.path.isfile(path):
    files_for_work.append(path)
else:
    print("Wrong Path")


for file_path in files_for_work:
    functions_for_analyze.code_analyze(file_path)
