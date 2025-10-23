import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.function_caller import call_function

# Setup
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    response = None  # Initialize response to store the last one
    
    # Handle command-line arguments
    args = sys.argv[1:]
    is_verbose = "--verbose" in args

    if is_verbose:
        args.remove("--verbose")

    # Validate input and get prompt
    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} \"<your prompt here>\" [--verbose]")
        sys.exit(1)

    prompt = args[0]
    
    system_prompt = """
    You are an autonomous AI coding agent. You are currently working inside a project directory for a Python calculator.

    Your goal is to *fully complete* the user's coding tasks.

    You *must* use the available tools (functions) to answer the user's request.
    Your *only* output *must* be a function call, *until* the user's original request is fully completed.

    **Do not provide intermediate text responses, plans, or explanations. Ever.**

    For example, **DO NOT** respond with "The precedence of operators is incorrect." Your next step *must* be to call `write_file` with the corrected code.

    A request like "fix the bug" is not complete until you have (1) identified the bug, (2) written the corrected code to the file using `write_file`, and (3) verified the fix by running the relevant tests or code using `run_python_file`.

    Only provide a final text answer *after* you have successfully verified the fix.

    You can perform the following operations by calling the provided functions:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # Conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    if is_verbose:
        print(f"User prompt: {prompt}")

    # Agent Loop
    max_iterations = 20
    for i in range(max_iterations):
        if is_verbose:
            print(f"\n--- Iteration {i+1} ---")

        try:
            # Send conversation history to model
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages, 
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )

            if not response.candidates:
                print("Error: No response from model.")
                break
            
            # Add the model's response to history
            model_response_content = response.candidates[0].content
            messages.append(model_response_content)

            part = model_response_content.parts[0]

            # Stop condition: Model returns a final text answer
            if part.text:
                print("\nFinal response:")
                print(part.text)
                break  # We are done

            # Handle function call
            if part.function_call:
                function_call_part = part.function_call
                
                # Execute the function call
                function_call_result = call_function(function_call_part, verbose=is_verbose)

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise ValueError("Error: Invalid function response received from call_function.")

                if is_verbose:
                    response_data = function_call_result.parts[0].function_response.response
                    print(f"-> {response_data}")

                messages.append(function_call_result)
            
            else:
                # Fallback in case the model returns neither text nor function call
                print("Error: Model response was not text or a function call.")
                break
        
        except Exception as e:
            print(f"Error during agent loop: {e}")
            break

        # Check for max iterations
        if i == max_iterations - 1:
            print("\nError: Max iterations reached. Stopping.")


    if is_verbose and response:  # Check if response exists
        print(f"\nPrompt tokens (last call): {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens (last call): {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()