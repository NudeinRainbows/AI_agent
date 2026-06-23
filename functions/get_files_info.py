import os
from functions.validate_target_path import validate_target_path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    result = validate_target_path(working_directory, directory)
    if result[:6] == "Error:": return result

    if not os.path.isdir(result):
        return f'Error: "{result}" is not a directory'

    with os.scandir(result) as entries:
        for entry in entries:
            if not entry is None:
                print(f" - {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}")

