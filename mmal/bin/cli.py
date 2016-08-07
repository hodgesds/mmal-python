from pkgutil import iter_modules
import argparse
import importlib
import os
import sys


def find_subcommands(subparsers):
    for _, mod_name, is_pkg in iter_modules([os.path.dirname(__file__)]):
        if not is_pkg and mod_name not in [sys.modules, 'cli']:
            mod_fullname = 'mmal.bin.{}'.format(mod_name)
            module = importlib.import_module(mod_fullname)
            if hasattr(module, 'mmal_cmd'):
                module.mmal_cmd(subparsers)


def main():
    parser = argparse.ArgumentParser(
        prog = "mmal",
        description = "mmal: Meteorological Middleware Application Layer",
    )

    subparsers = parser.add_subparsers()

    find_subcommands(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
