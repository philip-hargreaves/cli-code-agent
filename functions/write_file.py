import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes or overwrites a file with the given content inside a specified directory.

    Args:
        working_directory: The base directory where file operations are permitted.
        file_path: The relative path of the file to be written.
        content: The string content to write to the file.

    Returns:
        A string indicating success or an error message.
    """
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)

        # Prevent writing outside the working directory
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directories exist
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of a specified file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)