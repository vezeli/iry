"""
Configuration file.
"""
from typing import Dict, List

FIELDS: List = ["time", "name", "amount", "origin", "currency"]
DEFAULTS: Dict = {"origin": "Swish", "currency": "SEK"}
FILENAME: str = "vault"
