import os
import fnmatch
import re


def is_ignored(path, ignored_patterns):
    return any(fnmatch.fnmatch(path, pattern) for pattern in ignored_patterns)


def get_ignored_patterns(gitignore_file):
    ignored_patterns = {'.git','site-packages'}
    if os.path.isfile(gitignore_file):
        with open(gitignore_file, "r") as f:
            ignored_patterns.update(line.strip() for line in f if line.strip() and not line.startswith("#"))
    return ignored_patterns


def traverse_directory(dir_path, ignored_patterns):
    code_string = ""
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if not is_ignored(d, ignored_patterns)]
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as f:
                    code = f.read()
                    code_string += f"{file_path}\n{code}\n-\n"
    return code_string


def generate_directory_tree(start_path, ignored_patterns):
    tree_output = ""
    for root, dirs, files in os.walk(start_path):
        if is_ignored(root, ignored_patterns):
            dirs[:] = []
            continue

        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignored_patterns)]

        relevant_files = [f for f in files if not is_ignored(os.path.join(root, f), ignored_patterns) and f.endswith(".py")] # Modified to include only .py files
        if relevant_files:
            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_output += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for file in relevant_files:
                tree_output += f"{subindent}{file}\n"
    return tree_output


def generate_project_code(projects_file, ignored_patterns):
    if not os.path.isfile(projects_file):
        print(f"Error: {projects_file} not found.")
        return

    output_file = "project_code.txt"
    with open(projects_file, "r") as f:
        project_files = [line.strip() for line in f if line.strip()]

    with open(output_file, "w") as f:
        for file_path in project_files:
            if not os.path.isfile(file_path):
                print(f"Error: {file_path} not found in the specified projects.txt.")
                continue
            if not is_ignored(file_path, ignored_patterns):
                with open(file_path, "r") as project_file:
                    code = project_file.read()
                    f.write(f"{file_path}\n{code}\n-\n")


def create_projects_file(projects_file, root_dir, ignored_patterns):
    with open(projects_file, "w") as f:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignored_patterns)]
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if not is_ignored(file_path, ignored_patterns) and file_name.endswith(".py"): # Modified to include only .py files
                    f.write(f"{file_path}\n")


def generate_functions_and_classes(input_file, output_file, app_dir, ignored_patterns):
    with open(input_file, "r") as f:
        code_string = f.read()

    lines = code_string.split("\n")
    relevant_files = []

    for i, line in enumerate(lines):
        if line.endswith(".py") and not any(ignored_pattern in line for ignored_pattern in ignored_patterns):
            relevant_files.append(line.strip())

    directory_tree = generate_directory_tree(app_dir, ignored_patterns)

    output_string = ""
    for file_path in relevant_files:
        with open(file_path, "r") as f:
            file_content = f.read()

        # Extract imports
        imports = []
        for import_line in re.findall(r"^import\s.+", file_content, re.MULTILINE):
            imports.append(import_line.strip())
        for from_import_line in re.findall(r"^from\s.+import.+", file_content, re.MULTILINE):
            imports.append(from_import_line.strip())

        # Extract classes and functions
        class_functions = []
        for match in re.finditer(r"(class|def)\s+(\w+)\s*\(", file_content):
            function_type = match.group(1)
            function_name = match.group(2)
            function_comment = ""

            # Extract comment if available
            comment_match = re.search(fr"{function_name}.*\n\s*\"\"\"(.*)\"\"\"", file_content)
            if comment_match:
                function_comment = comment_match.group(1)

            class_functions.append((function_type, function_name, function_comment))

        output_string += f"{file_path} "

        # Add directory tree comment
        for directory in directory_tree:
            if directory in file_path:
                output_string += f"#{directory}\n"

        # Add imports
        if imports:
            output_string += "\n[imports] "
            output_string += ", ".join(imports)
            output_string += "\n"

        # Add classes and functions
        for function_type, function_name, function_comment in class_functions:
            output_string += f"{function_name}("
            function_params = re.search(f"{function_name}\((.*)\)", file_content).group(1).strip()
            output_string += function_params
            output_string += "):"
            output_string += f" return #{function_comment}" if function_comment else "\n"
            output_string += "\n"

    with open(output_file, "w") as f:
        f.write(output_string)

def main():
    root_dir = os.getcwd()
    app_dir = os.path.join(root_dir, "app")
    gitignore_file = os.path.join(root_dir, ".gitignore")
    all_code_file = os.path.join(root_dir, "all_code.md")
    functions_file = os.path.join(root_dir, "functions_and_classes.md")
    directory_tree_file = os.path.join(root_dir, "directory_tree.txt")
    projects_file = os.path.join(root_dir, "projects.txt")

    ignored_patterns = get_ignored_patterns(gitignore_file)

    with open(directory_tree_file, "w") as f:
        f.write(generate_directory_tree(root_dir, ignored_patterns))

    with open(all_code_file, "w") as f:
        f.write(traverse_directory(app_dir, ignored_patterns))

    if os.path.isfile(projects_file):
        generate_project_code(projects_file, ignored_patterns)
    else:
        create_projects_file(projects_file, root_dir, ignored_patterns)
        generate_project_code(projects_file, ignored_patterns)

    generate_functions_and_classes(all_code_file, functions_file, app_dir, ignored_patterns)


if __name__ == "__main__":
    main()

