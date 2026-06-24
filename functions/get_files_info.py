import os
from functions.validate_target_path import validate_target_path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    result = validate_target_path(working_directory, directory)
    if result[:6] == "Error:": return result

    if not os.path.isdir(result):
        return f'Error: "{result}" is not a directory'

    lines = []
    with os.scandir(result) as entries:
        for entry in entries:
            if not entry is None:
                lines.append(
                    f" - {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}"
                )

    return "\n".join(lines)

