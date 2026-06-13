import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def add_record(old, new):
    history = load_history()
    history.append({
        "old": old,
        "new": new,
        "time": datetime.now().isoformat()
    })
    save_history(history)


def pop_last():
    history = load_history()
    if not history:
        return None

    last = history.pop()
    save_history(history)
    return last