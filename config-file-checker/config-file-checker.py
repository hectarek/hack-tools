import os
import re

def scan_config_files(directory):
    sensitive_patterns = [
        r'password\s*=\s*["\'].*?["\']',
        r'api_key\s*=\s*["\'].*?["\']',
        r'secret_key\s*=\s*["\'].*?["\']',
    ]
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.conf', '.cfg', '.ini', '.env', '.yaml', '.yml')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            print(f"Sensitive information found in {filepath}: {match}")

if __name__ == "__main__":
    config_directory = input("Enter the directory to scan for configuration files: ")
    scan_config_files(config_directory)