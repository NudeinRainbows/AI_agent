import os
from functions.validate_target_path import validate_target_path
from config import FILE_SIZE_READ
#FILE_SIZE_READ = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    result = validate_target_path(working_directory, file_path)
    if result[:6] == "Error:": return result

    if not os.path.isfile(result):
        return f"Error: {result} is not a file"

    with open(result, 'r') as f:
        try:
            contents = f.read(FILE_SIZE_READ)
        except:
            return f"Error: could not read {result} contents"

        # After reading the first MAX_CHARS...
        if f.read(1):
            contents += f'[...File "{result}" truncated at {FILE_SIZE_READ} characters]'

    return contents


