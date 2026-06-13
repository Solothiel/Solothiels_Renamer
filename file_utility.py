import os
## Safe file operations

def rename_file(file_path, new_name):
    folder = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]

    new_path = os.path.join(folder, new_name + ext)

    if os.path.exists(new_path):
        raise FileExistsError("File already Exists")

    os.rename(file_path, new_path)
    return new_path

