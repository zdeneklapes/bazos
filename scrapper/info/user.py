import sys
from os import path

class User:
    def __init__(self, name: str, phone_number: str, email: str, password: str, psc: str, products_path: str):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.pasword = password
        self.psc = psc
        self.products_path = products_path


def get_user() -> User:
    if len(sys.argv) > 2 and path.isdir(sys.argv[1]):
        path_to_all = sys.argv[1]
    else:
        path_to_all = '/Users/zlapik/Documents/photos-archive/bazos'

    user_info = parse_yaml(filename=path.join(path_to_all, 'user.yml'))

    return User(name=user_info['name'],
                phone_number=user_info['phone_number'],
                email=user_info['email'],
                password=user_info['password'],
                psc=user_info['psc'],
                products_path=path_to_all)
