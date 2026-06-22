import os
#from ... import config
FILE_SIZE_READ = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_path = os.path.abspath(working_directory)
    try:
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
    except:
        return f"Error: could not create target dir from {abs_path} and {file_path}"

    try:
        valid_target_dir = os.path.commonpath([abs_path, target_file]) == abs_path
    except:
        return f"Error: could not verify common path between {abs_path} and {target_file}"

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except:
        return f"Error: could not verify {file_path} exists"

    with open(target_file, 'r') as f:
        try:
            contents = f.read(FILE_SIZE_READ)
        except:
            return f"Error: could not read {file_path} contents"

        # After reading the first MAX_CHARS...
        if f.read(1):
            contents += f'[...File "{file_path}" truncated at {FILE_SIZE_READ} characters]'

    return contents


