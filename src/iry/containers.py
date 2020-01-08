"""
Container objects that store data.
"""
from collections import UserList
from dataclasses import dataclass, asdict
from datetime import datetime
from numbers import Number
from typing import Union

from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

from iry import config


@dataclass
class Record:
    date: Union[datetime, str]
    name: str
    amount: Union[Number, str]
    origin: str
    currency: str

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = datetime.fromisoformat(self.date)
        self.amount = float(self.amount)


class Register(UserList):
    """Container that stores ``Record`` objects."""
    _fields = config.DATA_FIELDS
