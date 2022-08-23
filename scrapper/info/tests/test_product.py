from os import path
from ..product import Product
import pytest

FILE_DIR = path.dirname(__file__)

def test_images():
    assert len(Product(product_path=path.join(FILE_DIR, 'testing_data/dog')).images) == 1
