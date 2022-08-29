import os
from os import path

product_info = {
  'rubric': '>>RUBRIC',
  'category': '>>CATEGORY',
  'title': '>>TITLE',
  'price': '>>PRICE',
  'description': '>>DESCRIPTION',
}


class Product:
  def __init__(self, product_path):
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
          self.title = line.strip()
        elif product_info[current_product_info_key] == product_info['price']:
          self.price = line.strip()
        # NOTE: Only here we appending line, must be at the end of info.txt
        elif product_info[current_product_info_key] == product_info['description']:
          self.description += line


def get_all_products(products_path) -> [Product]:
  products = []
  for dir in os.listdir(path=products_path):
    product_path = path.join(products_path, dir)
    if path.isdir(product_path):
      products.append(Product(product_path=product_path))
    else:
      print(f"Skipping {dir}")
  return products


def validate_products():
  # TODO
  pass
