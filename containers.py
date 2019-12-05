"""
Container objects for storing data.
"""
from collections import deque, namedtuple
import itertools

"""
Containing information about a single transfer.
"""
Record = namedtuple("Record", "dtime name amount")


def make_rec(entry):
    return Record._make(entry)


class Register(deque):
    """Container for Records."""

    def as_table(self):
        """Print ``Register`` as a table."""
        vline = f"+{'='*30}+{'='*25}+{'='*10}+"
        row = "|{dtime:30}|{name:25}|{amount:10}|"
        for rec in self:
            print(vline)
            print(row.format(**rec._asdict()))
        else:
            print(vline)

    def compute_sum(self, val):
        """Print the sum of amount in ``Register``."""
        print(sum(val))

    @property
    def names(self):
        return [rec.name for rec in self[1:]]

    @property
    def amount(self):
        return [int(rec.amount) for rec in self[1:]]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(itertools.islice(self, index.start,
                                               index.stop, index.step))
        return collections.deque.__getitem__(self, index)

    def _find(self, val):
        """Returns record with ``val``."""
        pass
