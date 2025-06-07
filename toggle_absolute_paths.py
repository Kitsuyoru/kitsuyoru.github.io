import os
import re
import sys

ALLOWED_MODES = ['d', 'w']
MSG_INVALID_MODE = "Invalid mode. Please enter 'd' or 'w'."

def process_file(filepath, mode):
    try:
        with open(filepath, 'r', encoding='utf-8') as current_file:
            content = current_file.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='latin-1') as current_file:
                content = current_file.read()
        except (FileNotFoundError, PermissionError, IOError):
            print(f"Could not read file: {filepath}.")
            return

    if mode == 'd':
        # 'href="/' -> 'href="'
        new_content = re.sub(r'src="/', r'src="', re.sub(r'href="/', r'href="', content))
    elif mode == 'w':
        # 'href="' -> 'href="/'
        new_content = re.sub(r'src="([^/])', r'src="/\1', re.sub(r'href="([^/])', r'href="/\1', content))
    else:
        print(MSG_INVALID_MODE)
        return

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as current_file:
            current_file.write(new_content)
        print(f"Updated: {filepath}")


def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode not in ALLOWED_MODES:
            print(MSG_INVALID_MODE)
            sys.exit(1)
    else:
        while True:
            mode = input("Operation mode ([d]evelopment or [w]eb) >> ").lower()
            if mode in ALLOWED_MODES:
                break
            print(MSG_INVALID_MODE)

    print(f"Mode: {mode}")
    script_name = os.path.basename(__file__)

    for root, _, files in os.walk('.'):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.basename(filepath) == script_name:
                continue

            try:
                process_file(filepath, mode)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    main()
