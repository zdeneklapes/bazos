import argparse
from pathlib import Path
import sys
from typing import Dict, Any

from bazos.main import BazosScrapper, BazosUser

__version__ = "0.1.0"
__apiversion__ = "0.1.0"
__author__ = 'Zdenek Lapes'
__license__ = 'MIT'


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    # true/false
    parser.add_argument('--login',
                        action='store_true',
                        help='Login to bazos')
    parser.add_argument('--bazos',
                        action='store_true',
                        help='Use bazos')
    parser.add_argument('--add-only',
                        action='store_true',
                        help='Add only new products, not remove old ones')
    parser.add_argument('--print-rubrics',
                        action='store_true',
                        help='Print rubrics')
    parser.add_argument("--verbose",
                        action='store_true',
                        default=True,
                        help='Verbose')
    parser.add_argument("--delete-all",
                        action='store_true',
                        default=True,
                        help='Verbose')
    parser.add_argument("--create-all",
                        action='store_true',
                        default=True,
                        help='Verbose')
    # ?
    parser.add_argument('--items-path',
                        type=Path,
                        required=True,
                        nargs='?',
                        help='Path to products directory')
    parser.add_argument('--credentials-path',
                        type=Path,
                        required=True,
                        nargs='?',
                        help='Path to products directory')
    # +
    parser.add_argument('--country',
                        nargs="+",
                        help="What bazos country to use",
                        default=['cz', 'sk'])
    cli_args = vars(parser.parse_args())
    return cli_args


def main():
    cli_args = parse_cli_argument()

    if cli_args['verbose']:
        # print(f"==> CLI args: {cli_args}")
        print(' '.join(sys.argv))

    if cli_args['login']:
        bazos_user = BazosUser(
            country='cz', items_path=cli_args['items_path'],
            credentials_path=cli_args['credentials_path']
        )
        bazos_user.authenticate()
        bazos_user.save_user_credentials()

    if cli_args['bazos']:
        for country in cli_args['country']:
            if cli_args['verbose']:
                print(f"==> Processing country: {country}")

            # Check if user credentials exists
            user = BazosUser(
                country='cz', items_path=cli_args['items_path'],
                credentials_path=cli_args['credentials_path']
            )
            try:
                user.exists_user_credentials(raise_exception=True)
            except FileNotFoundError as e:
                print(e)
                sys.exit(1)

            if cli_args['print_rubrics']:
                bazos_scrapper = BazosScrapper(country=country, cli_args=cli_args, user=user)
                # bazos_scrapper.check_user_files_available()
                bazos_scrapper.load_page_with_cookies()
                # bazos_scrapper.check_authentication()
                bazos_scrapper.print_all_rubrics_and_categories()
                return

            bazos_scrapper = BazosScrapper(country=country, cli_args=cli_args, user=user)
            bazos_scrapper.load_page_with_cookies()

            # Restore advertisements
            if cli_args['delete_all']:
                bazos_scrapper.delete_advertisements()
            if cli_args['create_all']:
                bazos_scrapper.create_advertisements()
    sys.exit()


if __name__ == '__main__':
    main()
