import os
from .. import config

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_path = os.path.abspath(working_directory)
    try:
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
    except:
        return f"Error: could not create target dir from {abs_path} and {directory}"

    try:
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
    except:
        return f"Error: could not verify common path between {abs_path} and {target_dir}"

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    except:
        return f"Error: could not verify {target_dir} exists"

    if valid_target_dir:
        with os.scandir(target_dir) as entries:
            for entry in entries:
                if not entry is None:
                    print(f" - {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}")

