import os

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
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
    except:
        return f"Error: could not verify {target_dir} exists"

    if valid_target_dir:
        return f'Success: "{directory}" is within the working directory'

    return "no valid path walked"
