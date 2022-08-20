import os
import sys
import time
from os import path
from typing import Optional
from threading import Timer
from enum import Enum
import pickle
import random

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
from selenium.webdriver.support.ui import Select

from dotenv import load_dotenv

load_dotenv()

from refactor_info_txt import refactor_info_txt

# BUG: Some images are rotated

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


def wait_random_time():
    time.sleep(random.random() * 1)


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
    'price': '>>PRICE',
    'description': '>>DESCRIPTION',
}


class Product:
    def __init__(self, product_path):
        self.rubric = ''
        self.category = ''
        self.title = ''
        self.price = ''
        self.description = ''
        self.images = sorted(map(lambda x: path.join(product_path, 'photos', x),
                          next(os.walk(path.join(product_path, 'photos')))[2]))
        #
        self.load_product(product_dir=product_path)

    def get_current_section(self, line) -> str:
        for key, value in product_info.items():
            if value in line:
                return key

        raise Exception(f"Key not found: key={key}, value={value}, line={line}")

    def load_product(self, *, product_dir):
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


class BazosScrapper:
    def __init__(self, url: str = ''):
        self.url_bazos = 'https://www.bazos.cz/'
        self.url_moje_inzeraty = 'https://www.bazos.cz/moje-inzeraty.php'
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def save_authentication(self, user: User):
        self.driver.get(self.url_moje_inzeraty)

        # Prepare authentication
        telefon_input = self.driver.find_element(By.NAME, 'telefon')
        telefon_input.clear()
        telefon_input.send_keys(user.phone_number)
        click_submit_by_value(submits=self.driver.find_elements(By.NAME, 'Submit'), value='Ověřit')

        # Authenticate
        code_input = self.driver.find_element(By.NAME, 'klic')
        code_input.clear()
        code_input.send_keys(input('Please provide authentification code sended to your phone: '))
        click_submit_by_value(submits=self.driver.find_elements(By.NAME, 'Submit'), value='Odeslat')

        # Save cookies
        pickle.dump(self.driver.get_cookies(), open(Settings.COOKIES_FILE, "wb"))
        # Save Local Storage
        pickle.dump(self.driver.execute_script("return window.localStorage;"), open(Settings.LOCAL_STORAGE_FILE, "wb"))

    def remove_advertisment(self, user: User):
        self.driver.find_element(By.CLASS_NAME, 'inzeratydetdel').find_element(By.TAG_NAME, 'a').click()
        self.driver.find_element(By.NAME, 'heslobazar').clear()
        self.driver.find_element(By.NAME, 'heslobazar').send_keys(user.pasword)
        click_submit_by_value(self.driver.find_elements(By.NAME, 'administrace'), 'Vymazat')

    def remove_advertisements(self, user: User):
        self.load_page_with_cookies(url=self.url_moje_inzeraty)
        self.driver.get(self.url_moje_inzeraty)
        while len(self.driver.find_elements(By.CLASS_NAME, 'nadpis')) != 0:
            wait_random_time()
            self.driver.find_element(By.CLASS_NAME, 'nadpis').find_element(By.TAG_NAME, 'a').click()
            wait_random_time()
            self.remove_advertisment(user=user)
            wait_random_time()

    def add_advertisement(self, product: Product, user: User):
        Select(self.driver.find_element(By.NAME, 'rubrikyvybrat')).select_by_visible_text(product.rubric)
        Select(self.driver.find_element(By.ID, 'category')).select_by_visible_text(product.category)

        wait_random_time()
        self.driver.find_element(By.ID, 'nadpis').send_keys(product.title)
        self.driver.find_element(By.ID, 'popis').send_keys(product.description)
        self.driver.find_element(By.ID, 'cena').send_keys(product.price)

        wait_random_time()
        self.driver.find_element(By.ID, 'lokalita').clear()
        self.driver.find_element(By.ID, 'lokalita').send_keys(user.psc)
        self.driver.find_element(By.ID, 'jmeno').clear()
        self.driver.find_element(By.ID, 'jmeno').send_keys(user.name)
        self.driver.find_element(By.ID, 'telefoni').clear()
        self.driver.find_element(By.ID, 'telefoni').send_keys(user.phone_number)
        self.driver.find_element(By.ID, 'maili').clear()
        self.driver.find_element(By.ID, 'maili').send_keys(user.email)
        self.driver.find_element(By.ID, 'heslobazar').clear()
        self.driver.find_element(By.ID, 'heslobazar').send_keys(user.pasword)

        wait_random_time()
        self.driver.find_element(By.CLASS_NAME, 'ovse').click()
        self.driver.find_element(By.NAME, 'souborp[]').send_keys('\n'.join(product.images))

        wait_random_time()
        click_submit_by_value(submits=self.driver.find_elements(By.NAME, 'Submit'), value='Odeslat')

    def go_to_rubric(self, product: Product):
        sections = self.driver.find_elements(By.CLASS_NAME, 'iconstblcell')
        for icon in sections:
            a = icon.find_element(By.TAG_NAME, 'a')
            if a.accessible_name == product.rubric:
                a.click()
                break

    def add_advertisements(self, user: User):
        self.load_page_with_cookies(url=self.url_moje_inzeraty)
        for dir in os.listdir(path=user.products_path):
            print(dir)

            wait_random_time()
            self.driver.find_element(By.CLASS_NAME, 'pridati').click()  # go to add page
            product_path = path.join(user.products_path, dir)
            product = Product(product_path=product_path)

            wait_random_time()
            self.go_to_rubric(product=product)
            self.add_advertisement(product=product, user=user)

    def load_page_with_cookies(self, url: str = ''):
        self.driver.get(self.url_moje_inzeraty)
        for cookie_dict in pickle.load(open('cookies.pkl', 'rb')):
            self.driver.add_cookie(cookie_dict)

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

    # Prepare Cookies
    if not os.path.isfile(Settings.COOKIES_FILE) or not os.path.isfile(Settings.LOCAL_STORAGE_FILE):
        bazos_scrapper.save_authentication(user=user)

    # Restore advertisements
    bazos_scrapper.remove_advertisements(user=user)
    bazos_scrapper.add_advertisements(user=user)


if __name__ == '__main__':
    main()
