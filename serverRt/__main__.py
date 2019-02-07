# -*- coding: utf-8 -*-
from aiohttp import web
from argparse import ArgumentParser
from .server import server_init


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--port",
        help="port", type=int, default=5005
    )
    arg_parser.add_argument(
        "--folder",
        help="folder", type=str, default="None"
    )
    args = arg_parser.parse_args()
    web.run_app(app=server_init(args), port=args.port)


if __name__ == '__main__':
    main()
