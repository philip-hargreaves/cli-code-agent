import os
import subprocess
import sys

def run_python_file(working_directory: str, file_path: str, args: list = None) -> str:
    """
    Executes a specified Python file within a working directory using a subprocess.

    Args:
        working_directory: The base directory where operations are permitted.
        file_path: The relative path of the Python file to execute.
        args: A list of string arguments to pass to the Python script.

    Returns:
        A string containing the STDOUT and STDERR, or an error message.
    """
    if args is None:
        args = []

    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check for file existance
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute file
        command = [sys.executable, full_path] + args
        
        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,  
            timeout=30,           
            capture_output=True,  
            text=True             
        )

        # Format output
        output = []
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        if stdout:
            output.append(f"STDOUT:\n{stdout}")
        
        if stderr:
            output.append(f"STDERR:\n{stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        if not output:
            return "No output produced."

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error executing Python file: {e}"