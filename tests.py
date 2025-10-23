from functions.run_python_file import run_python_file

def main():
    """
    Tests the run_python_file function with various cases.
    """
    print("--- Test 1: Running main.py (no args) ---")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print("-" * 30)

    print("\n--- Test 2: Running main.py with args ---")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print("-" * 30)

    print("\n--- Test 3: Running calculator/tests.py ---")
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print("-" * 30)

    print("\n--- Test 4: Attempting directory traversal ---")
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print("-" * 30)

    print("\n--- Test 5: Attempting non-existent file ---")
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)
    print("-" * 30)

    print("\n--- Test 6: Attempting non-Python file ---")
    result6 = run_python_file("calculator", "lorem.txt")
    print(result6)
    print("-" * 30)

if __name__ == "__main__":
    main()