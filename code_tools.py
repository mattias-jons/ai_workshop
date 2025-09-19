import os
import re


def add_or_replace_function(file_path: str, function_code: str) -> str:
    function_name_match = re.match(r"def\s+(\w+)\(", function_code)
    if not function_name_match:
        return "Invalid function definition."
    function_name = function_name_match.group(1)

    with open(file_path, "r") as f:
        lines = f.readlines()

    pattern = re.compile(rf"^def\s+{function_name}\(")
    start, end = -1, -1

    for i, line in enumerate(lines):
        if pattern.match(line):
            start = i
        elif start != -1 and line.strip().startswith("def "):
            end = i
            break

    if start != -1:
        end = end if end != -1 else len(lines)
        lines[start:end] = [function_code + "\n"]
    else:
        if not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append("\n" + function_code + "\n")

    with open(file_path, "w") as f:
        f.writelines(lines)

    return f"Function '{function_name}' updated in {file_path}"


def update_dict(file_path: str, dict_name: str, new_entry: str) -> str:
    with open(file_path, "r") as f:
        lines = f.readlines()

    start_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{dict_name} ="):
            start_idx = i
            break

    if start_idx == -1:
        return f"Dictionary '{dict_name}' not found."

    # Naive update: append new entry to next lines after dict_name = {
    for i in range(start_idx, len(lines)):
        if lines[i].strip().startswith("}"):
            lines.insert(i, f"    {new_entry},\n")
            break

    with open(file_path, "w") as f:
        f.writelines(lines)

    return f"Entry '{new_entry}' added to dict '{dict_name}' in {file_path}'"
