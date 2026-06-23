
import os

def validate_target_path(working_directory: str, path: str) -> str:
    abs_path = os.path.abspath(working_directory)
    try:
        target = os.path.normpath(os.path.join(abs_path, path))
    except:
        return f"Error: could not create target dir from {abs_path} and {path}"

    try:
        valid_target = os.path.commonpath([abs_path, target]) == abs_path
    except:
        return f"Error: could not verify common path between {abs_path} and {target}"

    if not valid_target:
        return f'Error: Cannot read "{path}" as it is outside the permitted working directory'

    return target

