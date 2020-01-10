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

    pklfile_path = pathlib.Path(pklfile)
    target_path = config.select("data", priority_file=pklfile)
    ctx.obj["TARGET"] = target_path
    config_file = config.select("config", priority_file=cfgfile)
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
    for rec in records:
        db.insert_record(rec, strategy="bisect")
    io_utils.write(db, target)


@cli.command()
@click.option("-f", "--field", "fields", default=None, help="field to display", multiple=True)
@click.option("--header", is_flag=True, help="list available fields")
@click.pass_context
def show(ctx, fields: List[str], header: bool):
    iryconfig = ctx.obj["CONFIG"]
    target = ctx.obj["TARGET"]
    if not target.exists():
        target_name = pathlib.PurePath(target).name
        msg = f"Ups, it seems that file \"{target_name}\" doesn't exist."
        print(msg)
        sys.exit(0)

    db = io_utils.read(target)
    if header:
        utils.list_fields(db)
        sys.exit(0)

    # TODO: make a class Table and clean this code
    attrs = iryconfig.attrs
    d = utils.table_shape(db, attrs)
    if not fields:
        fields = iryconfig.fields
    for rec in db:
        rv = {}
        for key, val in utils.gen_fields(rec, attrs):
            rv[key] = val
        utils.make_table(rv, d, fields)


if __name__ == "__main__":
    cli()
