import os
from functions.validate_target_path import validate_target_path
from config import FILE_SIZE_READ
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file in a specified directory relative to the working directory, returning up to 'FILE_SIZE_READ' (defined in ./config.py) characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    result = validate_target_path(working_directory, file_path)
    if result[:6] == "Error:": return result

    if not os.path.isfile(result):
        return f"Error: {result} does not exist or is not a file"

    with open(result, 'r') as f:
        try:
            contents = f.read(FILE_SIZE_READ)
        except:
            return f"Error: could not read {result} contents"

        # After reading the first MAX_CHARS...
        if f.read(1):
            contents += f'[...File "{result}" truncated at {FILE_SIZE_READ} characters]'

    return contents


