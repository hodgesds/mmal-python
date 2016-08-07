from mmal.server import run_server
from mmal.service import BaseMmalRPC, MmalRPCSqlAlchemy

def mmal_cmd(subparsers):
    server_subparser = subparsers.add_parser('server')
    server_subparser.set_defaults(func=main)
    server_subparser.add_argument(
        '-p', '--port',
        default = 8080,
        help    = 'Default port',
    )
    server_subparser.add_argument(
        '-d', '--dsn',
        default = '',
        help    = 'SQL dsn',
    )

def main(args):
    if len(args.dsn) > 0:
        rpc = MmalRPCSqlAlchemy()
        rpc.connect(args.dsn)
        run_server(args.port, rpc)
    else:
        run_server(args.port, BaseMmalRPC())

