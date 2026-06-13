import os
import re

def generate_suggestions(filename):
    name, _ =os.path.splitext(filename)

    name = name.replace("_", " ")
    name = name.replace("-", " ")
    name = re.sub(r"\(\d+\)", "", name)
    name = re.sub(r"\s+", "", name).strip()

    return name.title()

