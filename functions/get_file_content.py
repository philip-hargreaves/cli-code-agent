import os
from config import MAX_FILE_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Reads the content of a specified file within a working directory.

    Args:
        working_directory: The base directory where operations are permitted.
        file_path: The relative path of the file to read.

    Returns:
        The file's content (potentially truncated) or an error message.
    """
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure the target is a regular file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r", encoding="utf-8") as f:
            # Read one extra character to efficiently check if the file exceeds the limit
            content = f.read(MAX_FILE_CHARS + 1)

        if len(content) > MAX_FILE_CHARS:
            truncated_content = content[:MAX_FILE_CHARS]
            return (
                truncated_content
                + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            )
        else:
            return content

    except UnicodeDecodeError:
        return f'Error: Cannot decode "{file_path}". It may be a binary file.'
    except Exception as e:
        return f"Error: {e}"