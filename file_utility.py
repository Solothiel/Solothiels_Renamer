import os
import re
from history_manager import add_record


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', "", name)


def rename_file(file_path, new_name):
    folder = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]

    new_name = sanitize(new_name.strip())

    if not new_name:
        raise ValueError("Empty filename")

    new_path = os.path.join(folder, new_name + ext)

    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(folder, f"{new_name} ({counter}){ext}")
        counter += 1

    os.rename(file_path, new_path)

    add_record(file_path, new_path)

    return new_path


def undo_rename(old, new):
    os.rename(new, old)