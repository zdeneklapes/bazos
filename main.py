import os
import sys
import time
from os import path
from typing import Optional
from threading import Timer
from enum import Enum
import pickle

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

from dotenv import load_dotenv

load_dotenv()

from refactor_info_txt import refactor_info_txt


class Settings:
    COOKIES_FILE = 'cookies.pkl'
    LOCAL_STORAGE_FILE = 'local_storage.pkl'


class User():
    def __init__(self, name: str, phone_number: str, email: str, password: str, psc: str, products_path: str):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.pasword = password
        self.psc = psc
        self.products_path = products_path


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


def wait_n_seconds(seconds: int):
    for i in range(seconds):
        time.sleep(1)
        sys.stdout.write(f"\rwaiting {i + 1}s, until {seconds}s")


def click_submit_by_value(submits: [WebElement], value: str):
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
        self.url_bazos = 'https://www.bazos.cz/'
        self.url_moje_inzeraty = 'https://www.bazos.cz/moje-inzeraty.php'
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def save_authentication(self, user: User):
        self.driver.get(self.url_moje_inzeraty)

        # Prepare authentication
        telefon_input = self.driver.find_element(By.NAME, 'telefon')
        telefon_input.send_keys(user.phone_number)
        click_submit_by_value(submits=self.driver.find_elements(By.NAME, 'Submit'), value='Ověřit')

        # Authenticate
        code_input = self.driver.find_element(By.NAME, 'klic')
        code_input.send_keys(input('Please provide authentification code sended to your phone: '))
        click_submit_by_value(submits=self.driver.find_elements(By.NAME, 'Submit'), value='Odeslat')

        wait_n_seconds(20)

        # Save cookies
        pickle.dump(self.driver.get_cookies(), open(Settings.COOKIES_FILE, "wb"))
        # Save Local Storage
        pickle.dump(self.driver.execute_script("return window.localStorage;"), open(Settings.LOCAL_STORAGE_FILE, "wb"))


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

    def add_advertisements(self, user: User):
        # Prepare page
        self.load_page_with_cookies(url=self.url_moje_inzeraty)
        self.driver.find_element(By.CLASS_NAME, 'pridati').click()  # go to add page
        wait_n_seconds(10)

        # Start adding
        # for dir in os.listdir(path=user.products_path):
        #     product_path = path.join(user.products_path, dir)
        #     product = Product(product_path=product_path)
        #     print(product.name)
        #     self.add_advertisement(path_dir=product_path, product_info=product)
        #     break

    def load_page_with_cookies(self, url: str):
        self.driver.get(url)
        # for cookie_dict in pickle.load(open('cookies.pkl', 'rb')):
        #     for key, value in cookie_dict.items():
        #         print({"name": key, "value": value})
                # self.driver.add_cookie({"name": key, "value": value})
            # break

        for key, value in pickle.load(open('cookies.pkl', 'rb'))[-1].items():
                print({"name": key, "value": value})
            # self.driver.add_cookie({"name": key, "value": value})

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def main():
    user = User(name='Zdenek', phone_number='773274707', email='zlapes@seznam.cz',
                password=os.getenv('USER_PASSWORD_KEY'), psc='60200',
                products_path='/Users/zlapik/Documents/photos-archive/bazos/main-zlapes')

    # refactor_info_txt(user.products_path)
    # return

    # Start advertising
    bazos_scrapper = BazosScrapper()
    if not os.path.isfile(Settings.COOKIES_FILE) or not os.path.isfile(Settings.LOCAL_STORAGE_FILE):
        bazos_scrapper.save_authentication(user=user)
        print(pickle.load(open(Settings.COOKIES_FILE, 'rb')))
        print(pickle.load(open(Settings.LOCAL_STORAGE_FILE, 'rb')))
    # bazos_scrapper.add_advertisements(user=user)


if __name__ == '__main__':
    main()
