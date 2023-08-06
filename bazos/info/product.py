import os
from os import path
from currency_converter import CurrencyConverter

product_info = {
    'rubric': '>>RUBRIC',
    'category': '>>CATEGORY',
    'title': '>>TITLE',
    'price': '>>PRICE',
    'description': '>>DESCRIPTION',
}


class CurrencyRates:
    def __init__(self):
        self.rates_default = {
            'CZKEUR': 0.04,
            'EURCZK': 25.5,
            'EURUSD': 1.2,
            'EURGBP': 0.9,

        }

    def get_rate(self, rate: str = "EURCZK") -> float:
        cc = CurrencyConverter()
        if len(rate) != 6:
            raise ValueError(
                f"Rate {rate} is not correct. Should be 6 characters long.")
        try:
            return cc.convert(1, rate[:3], rate[3:])
        except Exception:
            return self.rates_default[rate]


class Product:
    def __init__(self, product_path: str):
        self.product_path = product_path

        self.rubric = ''
        self.category = ''
        self.title = ''
        self.price = ''
        self.description = ''
        self.images = self.get_images()

        #
        self.load_product_info(product_dir=product_path)
        self.currency_rates = CurrencyRates()

    def get_images(self):
        images = sorted(map(lambda x: path.join(self.product_path, 'photos', x),
                            next(os.walk(path.join(self.product_path, 'photos')))[2]))
        return [filename for filename in images if
                filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

    def get_location_price(self, country: str) -> str:
        if country == 'sk':
            return str(int(int(self.price) / self.currency_rates.get_rate("EURCZK") - 1))
        elif country == 'cz':
            return self.price

    def get_current_section(self, line) -> str:
        for key, value in product_info.items():
            if value in line:
                return key

        raise Exception(
            f"Key not found: key={key}, value={value}, line={line}")

    def load_product_info(self, *, product_dir):
        # NOTE: Rewrite this shit code
        with open(file=path.join(product_dir, 'info.txt'), mode='r') as file:
            for line in file.readlines():
                if '>>' in line:
                    current_product_info_key = self.get_current_section(
                        line=line)
                    continue

                if line.replace(' ', '').replace('\t', '').replace('\n', '') == '':
                    continue

                if product_info[current_product_info_key] == product_info['rubric']:
                    self.rubric = line.strip()
                elif product_info[current_product_info_key] == product_info['category']:
                    self.category = line.strip()
                elif product_info[current_product_info_key] == product_info['title']:
                    # Bazos doesn't support longer title than 60 chars
                    self.title = line[:60].strip()
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
    products = [Product(product_path=path.join(products_path, d))
                for d in dirs]

    print(f"Product loaded: {len(products)}")
    return products


def validate_products():
    # TODO
    pass
