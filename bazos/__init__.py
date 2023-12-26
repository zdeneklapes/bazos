import argparse
from pathlib import Path
import sys
from typing import Dict, Any
from distutils.util import strtobool  # noqa

from bazos.scrapper import BazosScrapper, BazosUser, BazosDriver

__version__ = "0.1.0"
__apiversion__ = "0.1.0"
__author__ = 'Zdenek Lapes'
__license__ = 'MIT'


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    BOOL_AS_STR_ARGUMENTS_FALSE = dict(
        type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True
    )
    BOOL_AS_STR_ARGUMENTS_TRUE = dict(
        type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True
    )
    # true/false
    parser.add_argument('--login',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Login to bazos')
    parser.add_argument('--bazos',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Use bazos')
    parser.add_argument('--print-rubrics',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Print rubrics')
    parser.add_argument("--verbose",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Verbose')
    parser.add_argument("--delete-all",
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Verbose')
    parser.add_argument("--create-all",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Verbose')
    parser.add_argument('--remote',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Use remote')
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
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_cli_argument()

    # Print arguments
    if args['verbose']:
        print(' '.join(sys.argv))

    # Driver
    bazos_driver = BazosDriver(args=args, country='cz')

    # Login
    if args['login']:
        bazos_user = BazosUser(country='cz', args=args, driver=bazos_driver.driver)
        bazos_user.authenticate()
        bazos_user.save_user_credentials()
    else:
        bazos_user = BazosUser(country='cz', args=args, driver=bazos_driver.driver)
        bazos_user.exists_user_credentials()

    # Rubrics
    if args['print_rubrics']:
        for country in args['country']:
            bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
            bazos_scrapper = BazosScrapper(country=country, args=args, user=bazos_user, driver=bazos_driver.driver)
            bazos_scrapper.load_page_with_cookies()
            bazos_scrapper.print_all_rubrics_and_categories()

    # Bazos
    if args['bazos']:
        for country in args['country']:
            bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)

            if args['verbose']:
                print(f"==> Processing country: {country}")

            bazos_scrapper = BazosScrapper(country=country, args=args, user=bazos_user, driver=bazos_driver.driver)
            bazos_scrapper.load_page_with_cookies()

            # Restore advertisements
            if args['delete_all']:
                bazos_scrapper.delete_advertisements()
            if args['create_all']:
                bazos_scrapper.create_advertisements()


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='.env')
    main()
