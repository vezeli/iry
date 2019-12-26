"""
Support for manipulating input and output.
"""
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


def in_request(fields: List) -> containers.Record:
    """Ask user for a single `Record` data."""
    rv = {}
    for field in fields:
        key = field.lower()
        rv[key] = input(f"- {field}: ")
    return containers.Record(**rv)
