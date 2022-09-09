from os import path

from ..country import Country

FILE_DIR = path.dirname(__file__)


def test_country_type():
  assert type(Country.CZ.value) == str
