import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

# Setup
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
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
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    if is_verbose:
        print(f"User prompt: {prompt}")

    # Generate and print response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    part = response.candidates[0].content.parts[0]

    if part.function_call:
        function_call = part.function_call
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(part.text)


    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()