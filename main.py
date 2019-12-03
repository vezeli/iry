"""
Main program.
"""
import argparse
import datetime

import containers
import io_utils


def init(args):
    filename = io_utils.pickle_file
    header = containers.Record("Transfer date", "Name", "Amount")
    io_utils.write(containers.Register([header]), filename)
    io_utils.read(filename)


def add(args):
    reg = io_utils.read()
    print('To add transfer provide the following form "full name amount"')
    for num in range(args.n):
        input_data = input("[{}] ".format(num))
        *name, amount = input_data.split()
        name = " ".join(name)
        dtime = str(datetime.datetime.now())
        data = {"dtime": dtime, "name": name, "amount": amount}
        entry = containers.Record(**data)
        reg.append(entry)
    io_utils.write(reg)


def remove(args):
    reg = io_utils.read()
    for _ in range(args.n):
        reg.pop()
    io_utils.write(reg)


parser = argparse.ArgumentParser(prog="iwime")
parser.add_argument("-ls", "--list", action="store_true", help="list all records")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help")

parser_add = subparsers.add_parser("add", help="add records")
parser_add.add_argument("n", type=int, help="number of records to add", default=1)
parser_add.set_defaults(func=add)

parser_remove = subparsers.add_parser("remove", help="remove records")
parser_remove.add_argument("n", type=int, help="number of records to remove", default=1)
parser_remove.set_defaults(func=remove)

parser_init = subparsers.add_parser("init", help="initialize records")
parser_init.set_defaults(func=init)

args = parser.parse_args()

if args.list:
    reg = io_utils.read()
    reg.as_table()
else:
    args.func(args)
