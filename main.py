"""
Main program.
"""
import argparse
import datetime

import containers
import io_utils


def init(args):
    filename = io_utils.pickle_file
    header = containers.Record("Date", "Name", "Amount", "Origin", "Currency")
    io_utils.write(containers.Register([header]), filename)
    io_utils.read(filename)


def add(args):
    reg = io_utils.read()
    print('To add transfer provide the following form "full name amount origin currency"')
    for num in range(args.n):
        input_data = input("[{}] ".format(num + 1))  # start counting from 1 and not 0
        *name, amount, origin, currency = input_data.split()
        name = " ".join(name)
        dtime = str(datetime.datetime.now())
        data = {"time": dtime, "name": name, "amount": amount, "origin":
                origin, "currency": currency}
        entry = containers.Record(**data)
        reg.append(entry)
    io_utils.write(reg)


def remove(args):
    reg = io_utils.read()
    for _ in range(args.n):
        reg.pop()
    io_utils.write(reg)


def show(args):
    reg = io_utils.read()
    if not any((args.sum, args.people, args.npeople)):
        reg.as_table()
    else:
        if args.sum:
            print("sum: " + reg.compute_sum(reg.amount))
        if args.people:
            names = set(reg.names)
            print("participants: " + ", ".join(sorted(names)))
        if args.npeople:
            print("number of participants: " + str(len(set(reg.names))))


parser = argparse.ArgumentParser(prog="iry")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help")

parser_add = subparsers.add_parser("add", help="add records")
parser_add.add_argument("n", type=int, help="number of records to add", default=1)
parser_add.set_defaults(func=add)

parser_remove = subparsers.add_parser("remove", help="remove records")
parser_remove.add_argument("n", type=int, help="number of records to remove", default=1)
parser_remove.set_defaults(func=remove)

parser_show = subparsers.add_parser("show", help="show records")
parser_show.set_defaults(func=show)

parser_show.add_argument(
    "--table", action="store_true", help="list all records", default=True
)
parser_show.add_argument("--sum", action="store_true", help="return the final sum")
parser_show.add_argument("--people", action="store_true", help="return the final sum")
parser_show.add_argument("--npeople", action="store_true", help="return the final sum")

parser_init = subparsers.add_parser("init", help="initialize records")
parser_init.set_defaults(func=init)

args = parser.parse_args()

args.func(args)
