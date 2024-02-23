import argparse
from pathlib import Path
import sys
from typing import Any, Callable, Dict
from distutils.util import strtobool  # noqa

from bazos.scrapper import BazosScrapper, BazosUser, BazosDriver

__version__ = "0.1.0"
__apiversion__ = "0.1.0"
__author__ = 'Zdenek Lapes'
__license__ = 'MIT'


def parse_cli_argument() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    BOOL_AS_STR_ARGUMENTS_FALSE = dict(type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True)
    BOOL_AS_STR_ARGUMENTS_TRUE = dict(type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True)
    # true/false
    parser.add_argument('--login',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Login to bazos')
    parser.add_argument('--print-rubrics',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Print rubrics')
    parser.add_argument("--verbose",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Verbose')
    parser.add_argument("--delete-all",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Delete all advertisements')
    parser.add_argument("--create-all",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Create all advertisements')
    parser.add_argument("--update-all",
                        **BOOL_AS_STR_ARGUMENTS_TRUE,
                        help='Update all advertisements with updated data')
    parser.add_argument('--remote',
                        **BOOL_AS_STR_ARGUMENTS_FALSE,
                        help='Use remote')
    # Possible values: fast, slow
    parser.add_argument('--mode',
                        type=str,
                        choices=['fast', 'slow'],
                        default='fast',
                        nargs='?',
                        help='Mode')
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


def loop_country(args, bazos_driver, callback: Callable):
    for country in args['country']:
        if args['verbose']:
            print(f"\n==> Processing country: {country} =============================")

        bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
        bazos_scrapper = BazosScrapper(country=country, args=args, user=bazos_user, driver=bazos_driver.driver)
        bazos_scrapper.load_page_with_cookies()

        # Restore advertisements
        if args['delete_all']:
            bazos_scrapper.delete_all_advertisements()
        if args['create_all']:
            bazos_scrapper.create_all_advertisements()


def main():
    args = parse_cli_argument()

    # Print arguments
    if args['verbose']:
        print(' '.join(sys.argv))
        print(args)

    bazos_driver = BazosDriver(args=args, country='cz')
    for country in args['country']:
        if args['verbose']:
            print(f"==> Processing country: {country}")

        if args['login']:
            bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
            bazos_user.authenticate()
            bazos_user.save_user_credentials()
        else:
            bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
            bazos_user.exists_user_credentials()

        if args['print_rubrics']:
            bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
            bazos_scrapper = BazosScrapper(country=country, args=args, user=bazos_user, driver=bazos_driver.driver)
            bazos_scrapper.load_page_with_cookies()
            bazos_scrapper.print_all_rubrics_and_categories()

        if args['delete_all'] is False and args['create_all'] is False:
            break

        bazos_user = BazosUser(country=country, args=args, driver=bazos_driver.driver)
        bazos_scrapper = BazosScrapper(country=country, args=args, user=bazos_user, driver=bazos_driver.driver)
        bazos_scrapper.load_page_with_cookies()

        if args['delete_all']:
            bazos_scrapper.delete_all_advertisements()

        if args['create_all']:
            bazos_scrapper.create_all_advertisements()


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='.env')
    main()
