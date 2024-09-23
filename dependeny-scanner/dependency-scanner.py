# First, install the required package:
# pip install safety

import subprocess

def check_dependencies():
    try:
        result = subprocess.run(['safety', 'check'], capture_output=True, text=True)
        print(result.stdout)
        if "No known security vulnerabilities found" in result.stdout:
            print("No vulnerabilities found in dependencies.")
        else:
            print("Vulnerabilities found in dependencies. Please review the report above.")
    except Exception as e:
        print(f"Error running dependency check: {e}")

if __name__ == "__main__":
    check_dependencies()