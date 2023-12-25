import argparse
import sys
from typing import Dict, Any

from bazos.main import bazos_main as bz, BazosScrapper

__version__ = "0.1.0"
__apiversion__ = "0.1.0"
__author__ = 'Zdenek Lapes'
__license__ = 'MIT'


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--login',
                        action='store_true',
                        help='Login to bazos')
    parser.add_argument('-b', '--bazos',
                        action='store_true',
                        help='Use bazos')
    parser.add_argument('--add-only',
                        action='store_true',
                        help='Add only new products, not remove old ones')
    parser.add_argument('--print-rubrics',
                        action='store_true',
                        help='Print rubrics')
    parser.add_argument('--country',
                        nargs="+",
                        help="What bazos country to use",
                        default=['cz', 'sk'])
    parser.add_argument('-p', '--path',
                        help='Path to products directory')
    parser.add_argument("--update-credentials",
                        action='store_true',
                        help='Update credentials')
    cli_args = vars(parser.parse_args())
    return cli_args


def main():
    cli_args = parse_cli_argument()

    if cli_args['login']:
        bazos_scrapper = BazosScrapper(country=cli_args['country'][0], cli_args=cli_args)
        # bazos_scrapper.check_user_files_available()
        bazos_scrapper.save_authentication()
        bazos_scrapper.load_page_with_cookies()
        bazos_scrapper.check_authentication()
        return

    if cli_args['bazos']:
        bz(cli_args=cli_args)

    sys.exit()


if __name__ == '__main__':
    main()
