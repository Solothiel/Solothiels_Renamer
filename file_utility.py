import os
import re


## Safe file operations

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "", name)


def rename_file(file_path, new_name):
    folder = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]

    new_name = new_name.strip()

    if not new_name:
        raise ValueError("Filename cannot be empty")

    new_name = sanitize_filename(new_name)

    base_path = os.path.join(folder, new_name + ext)

    # prevent overwrite by auto-numbering
    new_path = base_path
    counter = 1

    while os.path.exists(new_path):
        new_path = os.path.join(folder, f"{new_name} ({counter}){ext}")
        counter += 1

    os.rename(file_path, new_path)
    return new_path
