import sys
from os import path
from typing import Union, Optional

from shared.utils import parse_yaml


# TODO: @dataclass maybe
class User:
  def __init__(self, products_path='/Users/zlapik/Documents/photos-archive/bazos'):
    if len(sys.argv) > 2 and path.isdir(sys.argv[1]):
      products_path = sys.argv[1]

    user_info = parse_yaml(filename=path.join(products_path, 'user.yml'))

    self.name = user_info['name']
    self.phone_number = user_info['phone_number']
    self.email = user_info['email']
    self.password = user_info['password']
    self.psc = user_info['psc']
    self.products_path = products_path
