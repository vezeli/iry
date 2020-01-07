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
@click.option("-p", "--pklfile", default=config.DEFAULT_DATA_FILE, help="select pickle file")
@click.option("-c", "--cfgfile", default=config.DEFAULT_CONFIG_FILE, help="select configuration file")
@click.pass_context
def cli(ctx, pklfile: str, cfgfile: str):
    ctx.ensure_object(dict)

    pklfile = pathlib.Path(pklfile)
    target_file = config.select("data", priority_path=pklfile)
    ctx.obj["TARGET"] = target_file
    config_file = config.select("config", priority_path=cfgfile)
    ctx.obj["CONFIG"] = config.load_config(config_file)


@cli.command()
@click.option("-q", "--quantity", default=1, help="number of records to add")
@click.option("--defaults/--no-defaults", default=True, help="fall back on default values")
@click.option("--now", is_flag=True, help="automatically set current time")
@click.pass_context
def add(ctx, quantity: int, defaults: bool, now):
    target = ctx.obj["TARGET"]
    iryconfig = ctx.obj["CONFIG"]

    if not defaults:
        iryconfig.defaults = dict()
    if now:
        ctime = datetime.datetime.now().isoformat(sep=" ", timespec="minutes")
        iryconfig.change_default(field="Date", value=ctime)
    records = [io_utils.ask_user(i+1, iryconfig) for i in range(quantity)]

    db = io_utils.read(target)
    db.extend(records)
    io_utils.write(db, target)


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
        defaults = iryconfig.defaults
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
