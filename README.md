# Gemini AI Coding Agent

This is a simple but powerful autonomous AI agent built with Python and Google's Gemini API. It can read files, write code, and execute scripts to autonomously complete complex coding and debugging tasks.

## Demo: Autonomous Bug Fix

The agent is pre-configured to work on a simple Python calculator (in the `/calculator` directory) which has a typical bug: it doesn't respect operator precedence (`3 + 7 * 2` incorrectly returns `20`).

You can give the agent a single prompt to fix this, and it will handle the entire process on its own.

**Run the Demo:**

```bash
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"
```

The agent will then autonomously:

1.  **Read:** Call `get_files_info` and `get_file_content` to understand the project and find the bug in `calculator/pkg/calculator.py`.
2.  **Write:** Call `write_file` to apply the corrected logic to the file.
3.  **Verify:** Call `run_python_file` to run the code with the test expression, confirming the fix (it now gets `17`).
4.  **Report:** Print a final "I've fixed the bug" message.

---

## ⚠️ Security Warning ⚠️

This agent is not a production-ready tool. It has been given powerful permissions to **read, write, and execute any file** within its hard-coded working directory (`./calculator`).

Be extremely careful if you modify the code to point at other directories. This agent can (and will) overwrite files, execute code, and do exactly what you ask it to, for better or worse.

---

## Setup

1.  **Clone the repo:**

    ```bash
    git clone https://github.com/philip-hargreaves/cli-code-agent
    cd your-repo-name
    ```

2.  **Install dependencies:**
    _(This project uses `uv` for package management, but you can use `pip`.)_

    ```bash
    # Create a virtual environment
    python -m venv .venv
    source .venv/bin/activate

    # Install packages
    uv pip install -r requirements.txt
    ```

3.  **Set your API Key:**
    Create a `.env` file in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

---

## Available functions

The agent operates by choosing from a set of simple, secure functions (tools):

- **`get_files_info(directory)`:** Lists files and directories.
- **`get_file_content(file_path)`:** Reads the content of a file.
- **`write_file(file_path, content)`:** Writes (or overwrites) a file.
- **`run_python_file(file_path, args)`:** Executes a Python script.

The core logic is in `main.py`, which implements a loop that:

1.  Sends the user prompt and conversation history to the Gemini model.
2.  Receives a "function call" request from the model.
3.  Executes that function using `functions/function_caller.py`.
4.  Sends the function's result back to the model.
5.  Repeats this loop until the model provides a final text answer.

---

## How to Generalise This Agent

Right now, the agent is **hard-coded** to work _only_ in the `./calculator` directory via a constant in `functions/function_caller.py`.

To generalise it, you would replace this hard-coded path to accept a directory path from the user, and then pass that path as an argument to `call_function` inside the agent loop.

```bash
# Example of a generalised call
uv run main.py --dir /path/to/another/project "your prompt here"
```
