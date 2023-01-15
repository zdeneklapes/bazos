from os import path

from scrapper.common.country import Country
from ..product import Product

FILE_DIR = path.dirname(__file__)


def test_images():
  assert len(Product(product_path=path.join(FILE_DIR, 'testing_data/dog'), country=Country.CZ).images) == 1
