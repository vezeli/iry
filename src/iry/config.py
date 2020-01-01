"""
Configuration file.
"""
from typing import Dict, List

FIELDS: List[str] = ["Date", "Name", "Amount", "Origin", "Currency"]
DEFAULTS: Dict = {"Origin": "Swish", "Currency": "SEK"}
STORE_FILE: str = "vault.pkl" # convert to Path object for more generalization
