# check_null.py
import os

def check_file_for_null(filename):
    try:
        with open(filename, 'rb') as f:
            content = f.read()
            if b'\x00' in content:
                print(f"NULL BYTES FOUND in: {filename}")
                return True
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return False

# Проверяем все .py файлы
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            full_path = os.path.join(root, file)
            check_file_for_null(full_path)