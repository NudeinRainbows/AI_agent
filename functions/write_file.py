import os
from functions.validate_target_path import validate_target_path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    result = validate_target_path(working_directory, file_path)
    if result[:6] == "Error:": return result

    test_path_list = result[::-1].split("/", maxsplit=1)

    if len(test_path_list) != 2:
        return f"Error: Invalid path, {result}"

    test_path = test_path_list[1][::-1]

    try:
        os.makedirs(test_path, exist_ok=True)
    except:
        return f"could not ensure parent directories for {test_path}"

    try:
        with open(result, 'w') as f:
            f.write(content)
    except:
        return f"Error: could not write contents to {result}"

    return f'Successfully wrote to "{result}" ({len(content)} characters written)'


