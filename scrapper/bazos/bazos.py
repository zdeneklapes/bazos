import os
import sys
import time
from os import path
from typing import Optional, Union, Dict
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
import yaml
from dotenv import load_dotenv

from info import (settings, User, Product, get_all_products)
from shared import (wait_random_time, wait_n_seconds, refactor_info_txt, parse_yaml)

load_dotenv()


################################################################################
# BUG: Some images are rotated


def click_submit_by_value(submits: [WebElement], value: str):
  for submit in submits:
    if submit.get_attribute('value') == value:
      submit.click()


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
    pickle.dump(self.driver.get_cookies(), open(settings.COOKIES_FILE, "wb"))
    # Save Local Storage
    pickle.dump(self.driver.execute_script("return window.localStorage;"), open(settings.LOCAL_STORAGE_FILE, "wb"))

  def remove_advertisment(self, user: User):
    self.driver.find_element(By.CLASS_NAME, 'inzeratydetdel').find_element(By.TAG_NAME, 'a').click()
    self.driver.find_element(By.NAME, 'heslobazar').clear()
    self.driver.find_element(By.NAME, 'heslobazar').send_keys(user.password)
    click_submit_by_value(self.driver.find_elements(By.NAME, 'administrace'), 'Vymazat')

  def remove_advertisements(self, user: User):
    self.load_page_with_cookies(url=self.url_moje_inzeraty)
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
    self.driver.find_element(By.ID, 'heslobazar').send_keys(user.password)

    # TODO: Not working
    # self.driver.find_element(By.ID, 'uploadbutton').click()
    # self.driver.find_element(By.ID, 'uploadbutton').send_keys('\n'.join(product.images))
    # wait_n_seconds(100)

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
    def product_already_advertised(product: Product) -> bool:
      self.load_page_with_cookies(url=self.url_moje_inzeraty)
      for nadpis in self.driver.find_elements(By.CLASS_NAME, 'nadpis'):
        if product.title in nadpis.text:
          return True
      return False

    self.load_page_with_cookies(url=self.url_moje_inzeraty)
    products = get_all_products(products_path=user.products_path)

    print("==> Adding advertisements")
    for product in products:
      if product_already_advertised(product):
        print(f"Skipping: {product.product_path}")
        continue

      print(f"Adding: {product.product_path}")

      # product not advertised ADD them
      wait_random_time()
      self.driver.find_element(By.CLASS_NAME, 'pridati').click()  # go to add page

      wait_random_time()
      self.go_to_rubric(product=product)
      self.add_advertisement(product=product, user=user)

  def load_page_with_cookies(self, url: str = ''):
    self.driver.get(self.url_moje_inzeraty)
    for cookie_dict in pickle.load(open(settings.COOKIES_FILE, 'rb')):
      self.driver.add_cookie(cookie_dict)
    self.driver.get(self.url_moje_inzeraty)

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.driver.quit()


def bazos():
  user = User()
  bazos_scrapper = BazosScrapper()

  # Prepare Cookies
  if not os.path.isfile(settings.COOKIES_FILE) or not os.path.isfile(settings.LOCAL_STORAGE_FILE):
    bazos_scrapper.save_authentication(user=user)

  # Restore advertisements
  if '--add-only' not in sys.argv:
    bazos_scrapper.remove_advertisements(user=user)

  bazos_scrapper.add_advertisements(user=user)


if __name__ == '__main__':
  bazos()
