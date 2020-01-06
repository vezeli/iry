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
    _header = config.DEFAULT_FIELDS

    def list(self):
        """lists data from `self`."""
        for rec in self:
            yield asdict(rec)

    def as_table(self):
        """Print ``Register`` as a table."""
        vline = f"+{'='*30}+{'='*25}+{'='*10}+"
        row = "|{date:30}|{name:25}|{amount:10}|"
        for rec in self:
            print(vline)
            print(row.format(**rec.__dict__))
        else:
            print(vline)

    def compute_sum(self, val):
        """Print the sum of amount in ``Register``."""
        return str(sum(val))

    @property
    def names(self):
        return [rec.name for rec in self[1:]]

    @property
    def amount(self):
        return [int(rec.amount) for rec in self[1:]]

    def _find(self, val):
        """Returns record with ``val``."""
        pass
