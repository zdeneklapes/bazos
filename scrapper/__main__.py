import argparse
import os
import sys
from os import path
from typing import Dict, Any, Callable
from glob import glob

from bazos.bazos import bazos


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bazos', action='store_true', dest='bazos', required=False)
    cli_args = vars(parser.parse_args())
    return cli_args


if __name__ == '__main__':
    cli_args = parse_cli_argument()

    if cli_args['bazos']:
        bazos()

    sys.exit()
