import os
import sys
import time
from os import path
from typing import Optional
from threading import Timer
from enum import Enum

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def wait_n_seconds(*, seconds: int):
    for i in range(seconds):
        time.sleep(1)
        sys.stdout.write(f"\rwaiting {i + 1}s, until {seconds}s")


def click_submit_by_value(*, submits: [WebElement], value: str):
    for submit in submits:
        if submit.get_attribute('value') == value:
            submit.click()


product_info = {
    'rubric': '>>RUBRIC',
    'category': '>>CATEGORY',
    'title': '>>TITLE',
    'description': '>>DESCRIPTION',
    'price': '>>PRICE',
    'psc': '>>PSC',
    'name': '>>NAME',
    'phone_number': '>>PHONE_NUMBER',
    'email': '>>EMAIL',
    'password': '>>PASSWORD'
}


class Product:
    def __init__(self, product_path):
        self.rubric = ''
        self.category = ''
        self.title = ''
        self.description = ''
        self.price = ''
        self.psc = ''
        self.name = ''
        self.phone_number = ''
        self.email = ''
        self.password = ''
        self.load_product(product_dir=product_path)

    def get_current_section(self, line) -> str:
        for key, value in product_info.items():
            if value in line:
                return key

        raise Exception(f"Key not found: key={key}, value={value}, line={line}")

    def load_product(self, *, product_dir):
        # NOTE: Rewrite this shit code

        print(product_dir)
        with open(file=path.join(product_dir, 'info.txt'), mode='r') as file:
            _continue = False
            for line in file.readlines():
                # get section
                if '>>' in line:
                    current_product_info_key = self.get_current_section(line=line)
                    _continue = False
                    continue

                # NOTE: if section should be only one line text continue until next section
                if _continue: continue

                # save
                if product_info[current_product_info_key] == product_info['rubric']:
                    self.rubric = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['category']:
                    self.category = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['title']:
                    self.title = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['description']:
                    self.description += line.strip()  # NOTE: Only here we appending line
                    _continue = True
                elif product_info[current_product_info_key] == product_info['price']:
                    self.price = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['psc']:
                    self.psc = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['name']:
                    self.name = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['phone_number']:
                    self.phone_number = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['email']:
                    self.email = line.strip()
                    _continue = True
                elif product_info[current_product_info_key] == product_info['password']:
                    self.password = line.strip()
                    _continue = True


class BazosScrapper:
    def __init__(self, url: str = ''):
        self.url = 'https://www.bazos.cz/'
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # def load_my_advertisements(self):
    def remove_all_advertisements(self):
        # TODO
        pass

    def add_advertisement(self, path_dir: str, product_info: Product):
        icons = self.driver.find_elements(By.CLASS_NAME, 'iconstblcell')
        for icon in icons:
            b = icon.find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'b')
            if b.text == product_info.rubric:
                icon.click()
                # TODO: I stuck here because "cookies or something else not working" and it need mobile check every time
                wait_n_seconds(seconds=5)

    def add_advertisements(self, path_dir: str):
        # Prepare page
        pridat = self.driver.find_element(By.CLASS_NAME, 'pridati')
        pridat.click()

        # Start adding
        for dir in os.listdir(path=path_dir):
            product_path = path.join(path_dir, dir)
            product = Product(product_path=product_path)
            print(product.name)
            self.add_advertisement(path_dir=product_path, product_info=product)
            break

    def load_cookies_on_url(self):
        # telefon_input.send_keys('773274707')
        self.driver.get(self.url)

        cookie_dict = {
            '__gsync': '1:YTU6Nzk6MTY1OTI3Nzg5NDYyOToxMToxNjU5MjY5NjUxMjQ0OmExMTphMjoxMDE6ODI0MzM4NDphMjoxMDc6ODI0MzM4NTphMjoxMDg6MzE0MjphMjoxMDk6ODI0MzM4NTphMjoxMTA6ODI0MzM4NTphMjoxMTE6MzE0MjphMjoxMTI6MzE0MjphMjoxMTM6ODI0MzM4NTphMjoxMTY6MDphMjoxMTc6MzE0MjphMjoxMTg6MzE0Mg__',
            '__gsync_gdpr': '1:YTU6bjpuOjE2NTk5ODQ3NTIzOTc6MTY1OTk4NDc1MjM5Nzpu',
            'bmail': 'zlapes%40seznam.cz',
            'bjmeno': 'Zdenek',
            'testcookieaaa': 'ano',
            '__gfp_64b': 'd_2FVk9XM1VVU2BcxgUmPLqO2utfTILgFEfRDQ4BT.z.C7|1659269650',
            'bid': '55054902',
            'testcookie': 'ano',
            'rekk': 'ano',
            'btelefon': '773274707',
            'testcookieaaa': 'ano',
            'bkod': '36HU739H18'
        }

        for key, value in cookie_dict.items():
            self.driver.add_cookie({"name": key, "value": value})

        self.driver.get(self.url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def main():
    url = "https://www.bazos.cz/moje-inzeraty.php"
    bazos_scrapper = BazosScrapper()
    # bazos_scrapper.load_cookies_on_url()
    bazos_scrapper.add_advertisements(path_dir='/Users/zlapik/Documents/photos-archive/bazos/main-zlapes')


if __name__ == '__main__':
    main()
