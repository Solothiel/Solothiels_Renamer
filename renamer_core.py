import os
import re

STOPWORDS = {"copy", "final", "new", "v1", "v2", "draft"}

def generate_suggestions(filename):
    name, _ = os.path.splitext(filename)

    name = name.replace("_", " ")
    name = name.replace("-", " ")

    name = re.sub(r"\(\d+\)", "", name)

    words = name.split()
    words = [w for w in words if w.lower() not in STOPWORDS]

    name = " ".join(words)
    name = re.sub(r"\s+", " ", name).strip()

    return name.title()
