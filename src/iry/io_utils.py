"""
Support for manipulating input and output.
"""
import pickle
from typing import Dict, List

from iry import config, containers

_defaults = config.DEFAULTS


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


def in_request(fields: List, allow_defaults: bool) -> containers.Record:
    """Ask user for single `Record` data."""
    #TODO: rewrite in a more understandable way
    global _defaults
    #TODO: change global _defaults to a function that searches for the default
    # value, if there are default in config, user config and maybe some
    # other place
    if not allow_defaults:
        _defaults = dict()
    rv = {}
    for field in fields:
        key = field.lower()
        if field in _defaults:
            rv[key] = _defaults[field]
        else:
            rv[key] = input(f"- {field}: ")
    return containers.Record(**rv)
