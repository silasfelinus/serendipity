import os
import fnmatch

# Define the paths to the directories and files
root_dir = os.getcwd()
app_dir = os.path.join(root_dir, "app")
gitignore_file = os.path.join(root_dir, ".gitignore")
all_code_file = os.path.join(root_dir, "all_code.md")
functions_file = os.path.join(root_dir, "functions_and_classes.md")

# Read the .gitignore file and extract patterns to ignore
ignored_patterns = set()
if os.path.isfile(gitignore_file):
    with open(gitignore_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ignored_patterns.add(line)

# Generate a string containing all the Python code in the app directory and its subdirectories
def traverse_directory(dir_path="."):
    code_string = ""

    for root, dirs, files in os.walk(dir_path):
        # Remove any subdirectories that match the ignored patterns
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignored_patterns)]

        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)

                with open(file_path, "r") as f:
                    code = f.read()
                    code_string += f"{file_path}\n{code}\n-\n"

    return code_string

# Write the Python code to all_code.md
with open(all_code_file, "w") as f:
    f.write(traverse_directory(app_dir))

# Extract relevant functions and classes from code_string and write them to functions_and_classes.md
def generate_functions_and_classes(code_string, output_file):
    lines = code_string.split("\n")
    relevant_lines = []
    relevant_files = set()

    for i, line in enumerate(lines):
        if line.startswith("# "):
            relevant_files.add(lines[i - 1])
            relevant_lines.append(line)
        elif (line.startswith("- def ") and "(" in line) or (line.startswith("- class ") and ":" in line):
            relevant_lines.append(line)

    output_string = "# Serendipity Functions and Classes\n\n"
    for file_path in relevant_files:
        output_string += f"**{file_path}**\n\n"
        for line in relevant_lines:
            if line.startswith("#") or line.startswith(f"- {file_path}"):
                output_string += f"{line}\n"
        output_string += "\n"

    with open(output_file, "w") as f:
        f.write(output_string)

# Generate the functions_and_classes.md file using all_code.md
with open(all_code_file, "r") as f:
    code_string = f.read()
generate_functions_and_classes(code_string, functions_file)
