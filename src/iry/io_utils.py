"""
Support functionality for manipulating input and output.
"""
import pathlib
import pickle
import sys
from typing import Dict, List, Optional

from iry import config, containers


def write(obj: containers.Register, file: pathlib.Path) -> None:
    if not file.exists():
        filename = pathlib.PurePath(file).name
        msg = f"File \"{filename}\" is created."
        print(msg)
    with open(file, "wb") as f:
        pickle.dump(obj, f)


def read(file: pathlib.Path) -> Optional[containers.Register]:
    try:
        with open(file, "rb") as f:
            obj = pickle.load(f)
        return obj
    except FileNotFoundError:
        return containers.Register()


def ask_user(record_num: int, required: List, defaults: Dict) -> Dict:
    """Store information from user input in ``dict``."""
    msg = f"Add record [{record_num}]:"
    print(msg)

    rv = dict()
    for field in required:
        key = field.lower()
        if field in defaults:
            rv[key] = defaults[field]
        else:
            if field == "Date":
                input_msg = f" - {field} (YYYY-MM-DD[ HH:MM]): "
            else:
                input_msg = f" - {field}: "
            rv[key] = input(input_msg)
    return rv
