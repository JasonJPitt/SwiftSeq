import os
import sys
import argparse

from importlib import import_module
from pkgutil import iter_modules

from swiftseq.core import commands


def execute_from_command_line():
    parser = argparse.ArgumentParser(prog='swiftseq')
    subparsers = parser.add_subparsers()

    commands_path = os.path.dirname(commands.__file__)
    subprograms = [
        [command] + command.info()
        for command
        in [import_module('swiftseq.core.commands.' + name) for _, name, _ in iter_modules([commands_path])]
    ]

    for module, command, description in subprograms:
        subp = subparsers.add_parser(
            command,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subp.set_defaults(func=module.main)
        module.populate_parser(subp)

    args = parser.parse_args()
    try:
        args.func(vars(args))
    except Exception as e:
        sys.stderr.write('An error occured:\n{}\n'.format(e))
