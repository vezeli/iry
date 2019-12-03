"""
Container objects for storing data.
"""
from collections import deque, namedtuple

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

    def _find(self, val):
        """Returns record with ``val``."""
        pass
