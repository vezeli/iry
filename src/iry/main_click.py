"""
CLI for `iry`.
"""
import click

from iry import __version__
from iry import config, containers, io_utils

_fields = config.FIELDS
_file = config.STORE_FILE


@click.group()
@click.version_option(__version__, "-V", "--version")
def cli():
    pass


@cli.command()
@click.option("-n", "--nrecords", default=1, help="Number of records to add")
@click.option("-f", "--filename", default=_file, help="File in which data is stored")
def add(nrecords: int, filename: str):
    data_obj = io_utils.read(filename)
    for n in range(nrecords):
        print(f"In [{n+1}]:")
        entry = io_utils.in_request(_fields)
        data_obj.append(entry)
    io_utils.write(data_obj, filename)


if __name__ == "__main__":
    cli()
