"""
Configuration file.
"""
from typing import Dict, List

FIELDS: List[str] = ["Date", "Name", "Amount", "Origin", "Currency"]
DEFAULTS: Dict = {"origin": "Swish", "currency": "SEK"}
STORE_FILE: str = "vault.pkl"
