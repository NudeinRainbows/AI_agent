import os
import subprocess
from functions.validate_target_path import validate_target_path
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes specified python file and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to pass to the python file",
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    result = validate_target_path(working_directory, file_path)
    if result[:6] == "Error:": return result
    if result[-3:] != ".py": return f'Error: "{file_path}" is not a Python file'

    if not os.path.isfile(result):
        return f"Error: \"{result.rsplit('/', maxsplit=1)[1]}\" does not exist or is not a file"

    command = ["python", result]
    if args: command.extend(args)

    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output_list = []

    if process.returncode != 0:
        output_list.append(f"Process exited with code {process.returncode}")

    if process.stdout == "" and process.stderr == "":
        output_list.append("No output produced")
    else:
        output_list.append(f"STDOUT: {process.stdout}")
        output_list.append(f"STDERR: {process.stderr}")

    return "".join(output_list)
