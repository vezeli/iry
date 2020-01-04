"""
CLI for `iry`.
"""
from pathlib import PurePath
import sys

import click

from iry import __version__
from iry import config, containers, io_utils, utils

_fields = config.FIELDS
_attrs = [val.lower() for val in config.FIELDS]
_file = config.STORE_FILE


@click.group()
@click.version_option(__version__, "-V", "--version")
def cli():
    pass


@cli.command()
@click.option("-n", "--nrecords", default=1, help="Number of records to add")
@click.option("-f", "--filename", default=_file, help="File in which data is stored")
@click.option("--defaults/--no-defaults", default=True, help="Consider the values of defalt fileds")
def add(nrecords: int, filename: str, defaults: bool):
    file = PurePath(filename)
    data_obj = io_utils.read(file)
    for n in range(nrecords):
        print(f"Entry [{n+1}]:")
        entry = io_utils.in_request(_fields, defaults)
        data_obj.append(entry)
    io_utils.write(data_obj, file)


@cli.command()
@click.option("--filename", default=_file, help="File in which data is stored")
@click.option("-f", "--fields", default=_fields, help="Fields to preview", multiple=True)
@click.option("--header/--no-header", default=False, help="Print field names only")
def show(filename: str, fields, header):
    file = PurePath(filename)
    data_obj = io_utils.read(file)
    if header:
        print(*data_obj._header)
        sys.exit(0)
    attrs = [field.lower() for field in fields]
    d = utils.table_shape(data_obj, attrs)
    for rec in data_obj:
        rv = {}
        for key, val in utils.gen_fields(rec, attrs):
            rv[key] = val
        utils.make_table(rv, d, fields)


if __name__ == "__main__":
    cli()
