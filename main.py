import argparse
import sys
from typing import Dict, Any

from scrapper.bazos import bazos as bz


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bazos', action='store_true')
    parser.add_argument('--add-only', action='store_true')
    parser.add_argument('--print-rubrics', action='store_true')
    parser.add_argument('--country', nargs="+")
    parser.add_argument('-p', '--path', dest='path', required=False, default='/Users/zlapik/Documents/photos-archive/bazos')
    cli_args = vars(parser.parse_args())
    return cli_args


if __name__ == '__main__':
    cli_args = parse_cli_argument()

    if cli_args['bazos']:
        bz(cli_args=cli_args)

    sys.exit()
