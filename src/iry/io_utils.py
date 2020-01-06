"""
Support for manipulating input and output.
"""
from pathlib import PurePath
import pickle
from typing import Dict, List

from iry import config, containers


def write(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)
    return None


def read(filename):
    try:
        with open(filename, "rb") as f:
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
            rv[key] = input(f"- {field}: ")
    return rv


def visual_output(file: PurePath):
    """Table that will store output."""
    pass
