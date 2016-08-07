from __future__ import print_function
import os
import sys
from mmal.client import Client


def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])

    return allparts


def mmal_cmd(subparsers):
    path = subparsers.add_parser('path')
    path_subparser(path)

    ping = subparsers.add_parser('ping')
    ping_subparser(ping)

    ts = subparsers.add_parser('ts')
    ts_subparser(ts)


def path_subparser(subparser):
    subparser.set_defaults(func=path_req)
    subparser.add_argument(
        '-p', '--port',
        default = os.environ.get('MMAL_PORT', 8080),
        help    = 'Default port',
    )
    subparser.add_argument(
        '--host',
        default = os.environ.get('MMAL_HOST', 'localhost'),
        help    = 'Default host',
    )
    subparser.add_argument(
        'path',
        default = [],
	nargs   = '*',
        help    = 'path',
    )


def ping_subparser(subparser):
    subparser.set_defaults(func=ping_req)
    subparser.add_argument(
        '-p', '--port',
        default = os.environ.get('MMAL_PORT', 8080),
        help    = 'Default port',
    )
    subparser.add_argument(
        '--host',
        default = os.environ.get('MMAL_HOST', 'localhost'),
        help    = 'Default host',
    )
    subparser.add_argument(
        'path',
        default = [],
	nargs   = '*',
        help    = 'path',
    )


def ts_subparser(subparser):
    subparser.set_defaults(func=ts_req)
    subparser.add_argument(
        '-p', '--port',
        default = os.environ.get('MMAL_PORT', 8080),
        help    = 'Default port',
    )
    subparser.add_argument(
        '--host',
        default = os.environ.get('MMAL_HOST', 'localhost'),
        help    = 'Default host',
    )
    subparser.add_argument(
        '-c', '--columns',
        default = [],
        action  = 'append',
        help    = 'Columns',
    )
    subparser.add_argument(
        '-o', '--offset',
        default = 0,
        type    = int,
        help    = 'Offset',
    )
    subparser.add_argument(
        '-l', '--limit',
        default = 10,
        type    = int,
        help    = 'Limit',
    )
    subparser.add_argument(
        'path',
        default = [],
	nargs   = '*',
        help    = 'path',
    )


def path_req(args):
    if len(args.path) == 0:
        sys.exit(1)

    paths = [ splitall(x) for x in args.path ]
    client = Client(args.host, args.port)

    print(client.path_request(paths))


def ping_req(args):
    paths = [ splitall(x) for x in args.path ]

    client = Client(args.host, args.port)

    print(client.ping_request(paths))


def ts_req(args):
    paths = [ splitall(x) for x in args.path ]

    client = Client(args.host, args.port)

    reply = client.ts_request(
        paths,
        cols   = args.columns,
        offset = args.offset,
        limit  = args.limit,
    )
    print(reply)
