import os
import logging


def read_gitignore():
    gitignore_set = set()
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    gitignore_set.add(line)
    return gitignore_set


def traverse_directory(gitignore_set, output_file, dir_path="."):
    for root, dirs, files in os.walk(dir_path):
        root = os.path.normpath(root)  # Normalize the root path
        root_parts = root.split(os.path.sep)

        if any(ignored in root_parts for ignored in gitignore_set):
            dirs[:] = []  # Skip traversal of ignored directories
            continue

        dirs[:] = [d for d in dirs if d not in gitignore_set]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                contents = []
                comment_printed = False  # Track if comment has been printed

                with open(file_path) as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()

                    if line.startswith('#') and not comment_printed:
                        contents.append(f"# {line[1:].strip()}")
                        comment_printed = True
                    elif (line.startswith('def ') and '(' in line) or (line.startswith('class ') and ':' in line):
                        contents.append(f"- {line}")
                    i += 1

                if len(contents) > 1:  # Only print if there are notable functions or classes
                    output_file.write(f"**{file_path}**\n")
                    output_file.write("\n".join(contents))
                    output_file.write("\n\n---\n\n")


def main():
    try:
        logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

        gitignore_set = read_gitignore()
        with open("serendipity_functions.md", "w") as output_file:
            output_file.write("# Serendipity Functions and Classes\n\n")
            traverse_directory(gitignore_set, output_file)
    except Exception as e:
        logging.exception("An error occurred: ")


if __name__ == "__main__":
    main()
