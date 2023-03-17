import os
import fnmatch


def read_gitignore():
    gitignore_set = set()
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    gitignore_set.add(line)
    return gitignore_set


def print_functions(gitignore_set, output_file):
    for root, _, files in os.walk('.'):
        if any(root.startswith(f"./{ignored}") for ignored in gitignore_set):
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                output_file.write(f"File: {file_path}\n")

                with open(file_path) as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()

                    if line.startswith('def'):
                        # If it's a function definition, write it to the output file
                        func = line
                        output_file.write(f"    {func}\n")
                        i += 1
                    else:
                        i += 1

                output_file.write('\n')


def print_comment(file_path, output_file):
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                output_file.write(f"    # {line[1:].strip()}\n")
                return


def traverse_directory(gitignore_set, output_file, dir_path="."):
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in gitignore_set]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                output_file.write(f"File: {file_path}\n")
                comment_printed = False  # Track if comment has been printed
                with open(file_path) as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()

                    if line.startswith('#'):
                        if not comment_printed:  # Print comment only once
                            output_file.write(f"    {line}\n")
                            comment_printed = True
                        i += 1
                    elif line.startswith('def'):
                        output_file.write(f"    {line}\n")
                        i += 1
                    else:
                        i += 1

                output_file.write('\n')


def main():
    try:
        gitignore_set = read_gitignore()
        with open("output.txt", "w") as output_file:
            traverse_directory(gitignore_set, output_file)
    except Exception as e:
        with open("error.log", "w") as error_file:
            error_file.write(str(e))


if __name__ == "__main__":
    main()
