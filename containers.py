"""
This file contains container objects in which the data is stored.
"""
from collections import deque
from dataclasses import dataclass, field
import datetime
import itertools
from typing import Union


@dataclass
class Record:
    time: datetime.datetime
    name: str
    amount: Union[int, float]
    origin: str
    currency: str


class Register(deque):
    """Container that stores ``Record`` objects."""

    def as_table(self):
        """Print ``Register`` as a table."""
        vline = f"+{'='*30}+{'='*25}+{'='*10}+"
        row = "|{time:30}|{name:25}|{amount:10}|"
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

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(
                itertools.islice(self, index.start, index.stop, index.step)
            )
        return collections.deque.__getitem__(self, index)

    def _find(self, val):
        """Returns record with ``val``."""
        pass
