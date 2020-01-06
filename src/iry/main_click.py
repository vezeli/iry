"""
CLI for `iry`.
"""
from pathlib import Path, PurePath
from typing import List, Optional
import sys

import click

from iry import __version__
from iry import config, containers, io_utils, utils



@click.group()
@click.version_option(__version__, "-V", "--version")
def cli():
    pass


@cli.command()
@click.option("-r", "--records", default=1, help="Number of records to be added.")
@click.option("-f", "--filename", default=config.DEFAULT_DATA_FILE, help="File in which data is stored.")
@click.option("--use-defaults/--no-defaults", default=True, help="Use default values to fill in records?")
@click.option("-c", "--configfile", default=config.DEFAULT_CONFIG_FILE, help="path to configuration file")
def add(records: int, filename: str, use_defaults: bool, configfile: Optional[str]):
    # TODO: provide a message when a new file is created
    file = PurePath(filename)
    data_obj = io_utils.read(file)

    # TODO: put configuration into context object and pass it to subcommands
    appname, appauthor = "iry", "vezeli"
    config_locations = config.app_location(appname, appauthor, "config")
    max_priority = min(config_locations.keys())
    increased_priority = max_priority - 1
    config_locations[increased_priority] = Path(configfile)
    configfile = config.determine_priority(config_locations)
    iryconfig = config.load_config(configfile)
    required = iryconfig.fields
    if use_defaults:
        defaults = iryconfig.field_values
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
@click.option("--filename", default=config.DEFAULT_DATA_FILE, help="File in which data is stored")
@click.option("-f", "--fields", default=None, help="Fields to preview", multiple=True)
@click.option("--header/--no-header", default=False, help="Print field names only")
@click.option("--use-defaults/--no-defaults", default=True, help="Use default values to fill in records?")
@click.option("-c", "--configfile", default=config.DEFAULT_CONFIG_FILE, help="path to configuration file")
def show(filename: str, fields: List[str], header: bool, configfile: str,
        use_defaults: bool):
    file = PurePath(filename)
    data_obj = io_utils.read(file)

    # TODO: put configuration into context object and pass it to subcommands
    appname, appauthor = "iry", "vezeli"
    config_locations = config.app_location(appname, appauthor, "config")
    max_priority = min(config_locations.keys())
    increased_priority = max_priority - 1
    config_locations[increased_priority] = Path(configfile)
    configfile = config.determine_priority(config_locations)
    iryconfig = config.load_config(configfile)
    required = iryconfig.fields
    if use_defaults:
        defaults = iryconfig.field_values
    else:
        defaults = dict()

    if not fields:
        fields = required

    if header:
        print(*data_obj._header)
        sys.exit(0)
    attrs = iryconfig.attrs
    d = utils.table_shape(data_obj, attrs)
    for rec in data_obj:
        rv = {}
        for key, val in utils.gen_fields(rec, attrs):
            rv[key] = val
        utils.make_table(rv, d, fields)


if __name__ == "__main__":
    cli()
