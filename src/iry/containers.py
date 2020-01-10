"""
Container objects that store data.
"""
from bisect import insort
from collections import UserList
from dataclasses import dataclass, asdict, field
from datetime import datetime
from numbers import Number
from typing import List, Union

from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

from iry import config


@dataclass(order=True)
class Record:
    date: Union[datetime, str] = field(repr=True, compare=True)
    name: str = field(repr=True, compare=True)
    currency: str = field(repr=False, compare=True)
    amount: Union[Number, str] = field(repr=False, compare=True)
    origin: str = field(repr=False, compare=False)

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = datetime.fromisoformat(self.date)
        self.amount = float(self.amount)


class Register(UserList):
    """Container class that holds data.

    This class holds ``Record`` instances and manipulates them.
    """
    _fields: List = config.DATA_FIELDS

    def insert_record(self, rec: Record, strategy="bisect") -> None:
        """Insert an ``Record`` to the ``self.data`` list.

        Depending on the value of ``insert_strategy`` ("append" or "bisect")
        insert a record in ``self.data`` using ``list.append`` or
        ``bisect.insort``. First method appends to the end of ``self.data``
        while the second one works only if the ``Register`` is sorted.
        """
        if strategy == "bisect":
            insort(self, rec)
        if strategy == "append":
            self.append(rec)
        return None
