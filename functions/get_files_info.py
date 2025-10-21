import os

def get_files_info(working_directory, directory="."):
    """
    Lists the contents of a specified directory within a working directory.

    Args:
        working_directory (str): The base directory where operations are permitted.
        directory (str): The relative path of the directory to list.

    Returns:
        str: A formatted string of the directory contents or an error message.
    """
    try:
        
        full_path = os.path.join(working_directory, directory)

        # Prevent directory traversal
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure the target is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # Get the list of items in the directory and format
        items = os.listdir(full_path)
        output_lines = []
        
        for item in items:
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            output_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {e}"