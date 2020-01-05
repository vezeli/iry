"""
CLI for `iry`.
"""
from pathlib import PurePath
import sys

import click

from iry import __version__
from iry import config, containers, io_utils, utils

#TODO: change _fields and _attrs to _fields dict that has field names and
# attributes in config.py
_fields = config.FIELDS
_attrs = [val.lower() for val in config.FIELDS]
_defaults = config.DEFAULTS
_file = config.STORE_FILE


@click.group()
@click.version_option(__version__, "-V", "--version")
def cli():
    pass


@cli.command()
@click.option("-r", "--records", default=1, help="Number of records to be added")
@click.option("-f", "--filename", default=_file, help="File in which data is stored")
@click.option("--use-defaults/--no-use-defaults", default=True, help="Take default values to fill in records")
def add(records: int, filename: str, use_defaults: bool):
    file = PurePath(filename)
    data_obj = io_utils.read(file)

    #TODO: change ``global _fileds, _defaults`` into a class that has all
    # default configuration from global config, user config and configuration
    # for a specific file.
    global _fields, _defaults
    required = list(_fields)
    if use_defaults:
        defaults = dict(_defaults)
    else:
        defaults = dict()

    rec_num = 1
    while True:
        record_info = io_utils.ask_user(rec_num, required, defaults)
        rec = containers.Record(**record_info)
        #TODO: change to bisect add and sorted ``Records`` and not append
        data_obj.append(rec)
        rec_num += 1
        if rec_num > records:
            break
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
