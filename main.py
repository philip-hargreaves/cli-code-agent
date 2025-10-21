import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    if is_verbose:
        print(f"User prompt: {prompt}")

    # Generate and print response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    print(response.text)

    # Print verbose metadata
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


# Main execution
if __name__ == "__main__":
    main()