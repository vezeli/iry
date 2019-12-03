"""
Support for manipulating input and output.
"""
import pickle

import config
import containers

pickle_file = config.FILENAME_BASE + ".pkl"


def write(obj, filename=pickle_file):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)
    return None


def read(filename=pickle_file):
    try:
        with open(filename, "rb") as f:
            obj = pickle.load(f)
        return obj
    except FileNotFoundError as e:
        print("Error: record.pkl not fould; initialize by running iwime init")
        raise e
