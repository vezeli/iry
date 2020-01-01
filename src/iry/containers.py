"""
Container objects that store data.
"""
from collections import deque
from dataclasses import dataclass, field, asdict
import datetime
import itertools
from typing import Union

from iry import config


@dataclass
class Record:
    date: datetime.datetime
    name: str
    amount: Union[int, float]
    origin: str
    currency: str


class Register(deque):
    """Container that stores ``Record`` objects."""
    _header = config.FIELDS

#   def locate(self):
#       """Lists data from `self`."""
#       fields = ["date", "name", "amount", "origin", "currency",]
#       rv = defaultdict(list)
#       # change None to object() like in Trey Hunters blog, maybe?
#       rv_size = {field: 0 for field in fields}
#       for rec in self:
#           for field in fields:
#               tmp = getattr(rec, field)
#               rv[field].append(tmp)
#               if len(tmp) > rv_size[field]:
#                   rv_size[field] = len(tmp)
#       return rv, rv_size

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

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(
                itertools.islice(self, index.start, index.stop, index.step)
            )
        return collections.deque.__getitem__(self, index)

    def _find(self, val):
        """Returns record with ``val``."""
        pass
