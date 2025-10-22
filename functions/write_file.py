import os

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