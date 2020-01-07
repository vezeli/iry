"""
Command-line interface (CLI) for `iry`.
"""
import datetime
import pathlib
import sys
from typing import List

import click

from iry import __version__
from iry import config, containers, io_utils, utils


@click.group()
@click.version_option(__version__, "-V", "--version")
@click.option("-p", "--pklfile", default=config.DEFAULT_DATA_FILE, help="pickle file")
@click.option("-c", "--cfgfile", default=config.DEFAULT_CONFIG_FILE, help="configuration file")
@click.pass_context
def cli(ctx, pklfile: str, cfgfile: str):
    ctx.ensure_object(dict)

    pklfile = pathlib.Path(pklfile)
    target_file = config.select("data", priority_path=pklfile)
    ctx.obj["TARGET"] = target_file

    config_file = config.select("config", priority_path=cfgfile)
    ctx.obj["CONFIG"] = config.load_config(config_file)


@cli.command()
@click.option("-r", "--records", default=1, help="Number of records to be added.")
@click.option("--use-defaults/--no-defaults", default=True, help="Use default values to fill in records?")
@click.option("--manual-time/--auto-time", default=False, help="set timestamp to now")
@click.pass_context
def add(ctx, records: int, use_defaults: bool, manual_time: bool):
    # TODO: auto-time and no-defaults will not work together, make a function
    # that adds defaults to a dictionary of defaults if no-defaults are turned
    # on
    file = ctx.obj["TARGET"]
    data_obj = io_utils.read(file)
    iryconfig = ctx.obj["CONFIG"]
    if not manual_time:
        now = datetime.datetime.now()
        now_fmt = now.isoformat(sep=" ", timespec="minutes")
        iryconfig.add_field_value("Date", now_fmt)
    required = iryconfig.fields
    if use_defaults:
        defaults = iryconfig.defaults_for_fields
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
@click.option("-f", "--fields", default=None, help="Fields to preview", multiple=True)
@click.option("--header", is_flag=True, help="Print field names only")
@click.option("--use-defaults/--no-defaults", default=True, help="Use default values to fill in records?")
@click.pass_context
def show(ctx, fields: List[str], header: bool, use_defaults: bool):
    file = ctx.obj["TARGET"]
    if not file.exists():
        filename = pathlib.PurePath(file).name
        msg = f"Ups, it seems that file \"{filename}\" doesn't exist."
        print(msg)
        sys.exit(0)
    data_obj = io_utils.read(file)
    iryconfig = ctx.obj["CONFIG"]
    required = iryconfig.fields
    if use_defaults:
        defaults = iryconfig.defaults_for_fields
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
