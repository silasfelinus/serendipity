import os
import fnmatch

def is_ignored(path):
    return any(fnmatch.fnmatch(path, pattern) for pattern in ignored_patterns)

# Define the paths to the directories and files
root_dir = os.getcwd()
app_dir = os.path.join(root_dir, "app")
gitignore_file = os.path.join(root_dir, ".gitignore")
all_code_file = os.path.join(root_dir, "all_code.md")
functions_file = os.path.join(root_dir, "functions_and_classes.md")
directory_tree_file = os.path.join(root_dir, "directory_tree.txt")

# Read the .gitignore file and extract patterns to ignore
ignored_patterns = set()
if os.path.isfile(gitignore_file):
    with open(gitignore_file, "r") as f:
        ignored_patterns = set(line.strip() for line in f if line.strip() and not line.startswith("#"))

def traverse_directory(dir_path="."):
    code_string = ""
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if not is_ignored(d)]
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as f:
                    code = f.read()
                    code_string += f"{file_path}\n{code}\n-\n"
    return code_string

def generate_directory_tree(start_path="."):
    tree_output = ""
    for root, dirs, files in os.walk(start_path):
        # Check if the current directory should be ignored
        if is_ignored(root):
            dirs[:] = []
            continue

        # Exclude ignored directories from the search
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]

        # Only add files that are not ignored
        relevant_files = [f for f in files if not is_ignored(os.path.join(root, f))]
        if relevant_files:
            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_output += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for file in relevant_files:
                tree_output += f"{subindent}{file}\n"
    return tree_output

with open(directory_tree_file, "w") as f:
    f.write(generate_directory_tree())

with open(all_code_file, "w") as f:
    f.write(traverse_directory(app_dir))

def generate_functions_and_classes(input_file, output_file):
    with open(input_file, "r") as f:
        code_string = f.read()

    lines = code_string.split("\n")
    relevant_lines = []
    relevant_files = set()

    for i, line in enumerate(lines):
        if line.startswith("# "):
            relevant_files.add(lines[i - 1])
        elif (line.startswith("- def ") and "(" in line) or (line.startswith("- class ") and ":" in line):
            relevant_lines.append(line)

    # Generate the directory tree
    directory_tree = generate_directory_tree(app_dir)

    # Append the directory tree to the output string
    output_string = f"# Directory Tree\n\n```\n{directory_tree}```\n\n# Serendipity Functions and Classes\n\n"
    
    for file_path in relevant_files:
        output_string += f"## {file_path}\n\n"
        output_string += f"### Functions\n\n"
        for line in relevant_lines:
            if line.startswith("- def ") and file_path in lines[i-1]:
                function_name = line.split("def ")[1].split("(")[0]
                output_string += f"* `{function_name}`\n"
        output_string += f"\n### Classes\n\n"
        for line in relevant_lines:
            if line.startswith("- class ") and file_path in lines[i-1]:
                class_name = line.split("class ")[1].split(":")[0]
                output_string += f"* `{class_name}`\n"
        output_string += "\n"

    with open(output_file, "w") as f:
        f.write(output_string)
        
generate_functions_and_classes(all_code_file, functions_file)