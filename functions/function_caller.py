from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Map functions
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

WORKING_DIRECTORY = "./calculator"

def call_function(function_call_part: types.FunctionCall, verbose=False):
    """
    Executes a function call requested by the LLM.

    Args:
        function_call_part: The FunctionCall object from the LLM's response.
        verbose: If True, prints detailed call and response information.

    Returns:
        A types.Content object with the function's result or an error.
    """
    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_to_call = FUNCTION_MAP[function_name]

    # Prepare arguments
    function_args = dict(args)
    function_args["working_directory"] = WORKING_DIRECTORY

    # Call functions
    try:
        function_result = function_to_call(**function_args)
        response_data = {"result": function_result}
    except Exception as e:
        response_data = {"error": f"Error executing function: {str(e)}"}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=response_data,
            )
        ],
    )