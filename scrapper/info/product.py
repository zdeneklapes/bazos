import os
from os import path

from colorama import Fore
from forex_python.converter import CurrencyRates

product_info = {
    'rubric': '>>RUBRIC',
    'category': '>>CATEGORY',
    'title': '>>TITLE',
    'price': '>>PRICE',
    'description': '>>DESCRIPTION',
}


class Product:
    def __init__(self, product_path: str, country: str):
        self.country = country
        self.product_path = product_path

        self.rubric = ''
        self.category = ''
        self.title = ''
        self.price = ''
        self.description = ''
        self.images = self.get_images()

        #
        self.load_product_info(product_dir=product_path)

    def get_images(self):
        images = sorted(map(lambda x: path.join(self.product_path, 'photos', x),
                            next(os.walk(path.join(self.product_path, 'photos')))[2]))
        return [filename for filename in images if
                filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

    def get_location_price(self, country: str) -> str:
        if country.lower() == "cz":
            return self.price
        elif country.lower() == "sk":
            price = str(int(int(self.price) / (CurrencyRates().get_rate('EUR', 'CZK') - 1)))
            return price

    def get_current_section(self, line) -> str:
        for key, value in product_info.items():
            if value in line:
                return key

        raise Exception(f"Key not found: key={key}, value={value}, line={line}")

    def load_product_info(self, *, product_dir):
        # NOTE: Rewrite this shit code
        with open(file=path.join(product_dir, 'info.txt'), mode='r') as file:
            for line in file.readlines():
                if '>>' in line:
                    current_product_info_key = self.get_current_section(line=line)
                    continue

                if line.replace(' ', '').replace('\t', '').replace('\n', '') == '':
                    continue

                if product_info[current_product_info_key] == product_info['rubric']:
                    self.rubric = line.strip()
                elif product_info[current_product_info_key] == product_info['category']:
                    self.category = line.strip()
                elif product_info[current_product_info_key] == product_info['title']:
                    self.title = line[:60].strip()  # Bazos doesn't support longer title than 60 chars
                elif product_info[current_product_info_key] == product_info['price']:
                    self.price = line.strip()
                # NOTE: Only here we append line, must be at the end of info.txt
                elif product_info[current_product_info_key] == product_info['description']:
                    self.description += line


def get_all_products(products_path: str, country: str) -> [Product]:
    print("==> Loading products")

    # Filter out all files and hidden directories
    dirs = [d for d in os.listdir(path=products_path)
            if path.isdir(path.join(products_path, d)) and d.startswith('.') is False]

    # Get ready all products
    products = [Product(product_path=path.join(products_path, d), country=country) for d in dirs]

    print(f"Product loaded: {len(products)}")
    return products


def validate_products():
    # TODO
    pass
