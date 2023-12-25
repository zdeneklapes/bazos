from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import pickle  # nosec
import sys
from os import path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from bazos.core import settings
from bazos.info.product import Product, get_all_products
from bazos.info.user import User
from bazos.shared.utils import wait_random_time
from bazos.info.rubric_category import get_rubric, get_category
from bazos.shared.utils import parse_yaml

load_dotenv()


################################################################################
# BUG: Some images are rotated, when you upload them to bazos

def click_submit_by_value(submits: [WebElement], value: str):
    for submit in submits:
        if submit.get_attribute('value') == value:
            submit.click()


class XPathsBazos:
    select_rubrik = "//div[@class='maincontent']/div[1]/form/select"
    select_category = "//div[@class='maincontent']/form/div[1]/select"
    user_inputs = "//div[@class='maincontent']/form/input"
    delete_pwd_input = "//div[@class='maincontent']/div[2]/form/input[1]"  # nosec
    delete_submit = "//div[@class='maincontent']/div[2]/form/input[4]"

    auth_phone_input = "//div[@class='maincontent']/form/input[2]"
    auth_phone_check_submit = "//div[@class='maincontent']/form/input[4]"
    auth_code_input = "//div[@class='maincontent']/div[1]/form/input[1]"
    auth_code_submit = "//div[@class='maincontent']/div[1]/form/input[3]"

    product_submit = "//div[@class='maincontent']/form/div/input[6]"
    product_rubric = "//div[@class='maincontent']/div[1]/form/select"
    product_category = "//div[@class='maincontent']/form/div[1]/select"
    product_img_input = "//div[@class='maincontent']/form/div[1]/input[3]"


class BazosDriver:
    def __init__(self, country: str, cli_args: dict):
        self.country = country
        self.cli_args = cli_args
        self.url_bazos = f"https://bazos.{country}"
        self.url_moje_inzeraty = path.join(self.url_bazos, 'moje-inzeraty.php')
        self.driver = self.get_driver()

    def set_chrome_options(self) -> Options:
        """Sets chrome options for Selenium.
            Chrome options for headless browser is enabled.
            """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        # options.binary_location = '/usr/bin/google-chrome'
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        #
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--log-level=DEBUG")
        # options.add_argument('--user-agent={}'.format(random.choice(list(self.user_agents))))
        return chrome_options

    def get_driver(self):
        options = self.set_chrome_options()
        webdriver_manager = ChromeDriverManager().install()
        service = Service(executable_path=webdriver_manager)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def __del__(self):
        self.driver.close()


class BazosUser:
    def __init__(self, country: str, products_path: str):
        self.country = country
        if len(sys.argv) > 2 and path.isdir(sys.argv[1]):
            products_path = sys.argv[1]

        user_info = parse_yaml(filename=path.join(
            products_path, f"user_{country}.yml"))

        self.name = user_info['name']
        self.phone_number = user_info['phone_number']
        self.email = user_info['email']
        self.password = user_info['password']
        self.psc = user_info['psc']
        self.products_path = products_path

    def check_user_files_available(self) -> None:
        if (not os.path.isfile(f"{settings.COOKIES_FILE}_{self.bazos_country}.pkl")  # nosec
                or not os.path.isfile(f"{settings.LOCAL_STORAGE_FILE}_{self.bazos_country}.pkl")):  # nosec
            print("==> User files not found, please login - login flag: --login")
            # self.save_authentication(user=self.user)

    def check_authentication(self) -> None:
        user_input = self.driver.find_elements(
            By.XPATH, XPathsBazos.user_inputs)
        # tel_input = self.driver.find_element(By.XPATH, XPathsBazos.auth_phone_input)
        if len(user_input) != 3:  # Mean is Authenticated, because there is not "Overit" button
            self.save_authentication(user=self.user)

    def save_authentication(self) -> None:
        self.driver.get(self.url_moje_inzeraty)

        # Prepare authentication
        telefon_input = self.driver.find_element(
            By.XPATH, XPathsBazos.auth_phone_input)
        telefon_input.clear()
        telefon_input.send_keys(self.user.phone_number)
        self.driver.find_element(
            By.XPATH, XPathsBazos.auth_phone_check_submit).click()  # Submit

        # Authenticate
        code_input = self.driver.find_element(
            By.XPATH, XPathsBazos.auth_code_input)
        code_input.clear()
        code_input.send_keys(
            input('Please provide authentification code sended to your phone: '))
        self.driver.find_element(
            By.XPATH, XPathsBazos.auth_code_submit).click()  # Submit

        # Save cookies
        pickle.dump(self.driver.get_cookies(),
                    file=open(f"{settings.COOKIES_FILE}_{self.bazos_country}.pkl", "wb"))  # nosec
        # Save Local Storage
        pickle.dump(self.driver.execute_script("return window.localStorage;"),
                    file=open(f"{settings.LOCAL_STORAGE_FILE}_{self.bazos_country}.pkl", "wb"))  # nosec


class BazosScrapper(BazosDriver):
    def __init__(self, country: str, cli_args: dict):
        super().__init__(country, cli_args)
        options = self.set_chrome_options()
        webdriver_manager = ChromeDriverManager().install()
        service = Service(executable_path=webdriver_manager)
        self.driver = webdriver.Chrome(service=service, options=options)

        # URLs
        self.user = User(country=country, products_path=cli_args['path'])
        self.bazos_country = country
        self.advertisements: int
        self.url_bazos = f"https://bazos.{country}"
        self.url_moje_inzeraty = path.join(self.url_bazos, 'moje-inzeraty.php')

    # def __del__(self):
    #     self.driver.close()

    def print_all_rubrics_and_categories(self):
        self.driver.find_element(
            By.CLASS_NAME, 'pridati').click()  # go to add page
        sections = self.driver.find_elements(By.CLASS_NAME, 'iconstblcell')
        sections[0].find_element(By.TAG_NAME, 'a').click()
        select_rubrik = Select(self.driver.find_element(
            By.XPATH, XPathsBazos.select_rubrik))

        _dict = {}
        rubric_options = [opt.text for opt in select_rubrik.options]
        for option in rubric_options:

            # Rubric
            Select(self.driver.find_element(
                By.XPATH, XPathsBazos.select_rubrik)).select_by_visible_text(option)

            # Category
            select_category = Select(self.driver.find_element(
                By.XPATH, XPathsBazos.select_category))
            _dict[option] = []
            for idx, category in enumerate(select_category.options):
                if idx == 0:
                    continue
                _dict[option].append(category.text)

        print(_dict)

    def load_page_with_cookies(self) -> None:
        self.driver.get(self.url_moje_inzeraty)
        for cookie_dict in pickle.load(open(f"{settings.COOKIES_FILE}_{self.bazos_country}.pkl", 'rb')):  # nosec
            self.driver.add_cookie(cookie_dict)
        self.driver.get(self.url_moje_inzeraty)

    def remove_advertisment(self, user: User):
        self.driver.find_element(By.CLASS_NAME, 'inzeratydetdel').find_element(
            By.TAG_NAME, 'a').click()
        pwd_input = self.driver.find_element(
            By.XPATH, XPathsBazos.delete_pwd_input)
        pwd_input.clear()
        pwd_input.send_keys(user.password)
        self.driver.find_element(
            By.XPATH, XPathsBazos.delete_submit).click()  # Submit-Delete

    def remove_advertisements(self, user: User):
        self.advertisements = len(
            self.driver.find_elements(By.CLASS_NAME, 'nadpis'))

        print("==> Removing old advertisements")
        for i in range(self.advertisements):
            element = self.driver.find_element(By.CLASS_NAME, 'nadpis')
            print(f"Removing[{i}/{self.advertisements}]: {element.text}")

            #
            wait_random_time()
            element.find_element(By.TAG_NAME, 'a').click()
            wait_random_time()
            self.remove_advertisment(user=user)
            wait_random_time()

    def add_advertisement(self, product: Product, user: User):
        # Rubrik
        select_rubrik = Select(self.driver.find_element(
            By.XPATH, XPathsBazos.product_rubric))
        select_rubrik.select_by_visible_text(
            get_rubric(self.bazos_country, product.rubric))

        # Product
        select_category = Select(self.driver.find_element(
            By.XPATH, XPathsBazos.product_category))
        select_category.select_by_visible_text(get_category(
            self.bazos_country, product.rubric, product.category))
        wait_random_time()
        self.driver.find_element(By.ID, 'nadpis').send_keys(product.title)
        self.driver.find_element(By.ID, 'popis').send_keys(product.description)
        self.driver.find_element(By.ID, 'cena').send_keys(
            product.get_location_price(self.bazos_country))

        wait_random_time()
        self.driver.find_element(By.ID, 'lokalita').clear()
        self.driver.find_element(By.ID, 'lokalita').send_keys(user.psc)
        self.driver.find_element(By.ID, 'jmeno').clear()
        self.driver.find_element(By.ID, 'jmeno').send_keys(user.name)
        self.driver.find_element(By.ID, 'telefoni').clear()
        self.driver.find_element(
            By.ID, 'telefoni').send_keys(user.phone_number)
        self.driver.find_element(By.ID, 'maili').clear()
        self.driver.find_element(By.ID, 'maili').send_keys(user.email)
        self.driver.find_element(By.ID, 'heslobazar').clear()
        self.driver.find_element(By.ID, 'heslobazar').send_keys(user.password)

        wait_random_time()
        self.driver.find_element(By.CLASS_NAME, 'ovse').click()
        self.driver.find_element(By.XPATH, XPathsBazos.product_img_input).send_keys(
            '\n'.join(product.images))

        wait_random_time()
        self.driver.find_element(By.XPATH, XPathsBazos.product_submit).click()

    def add_advertisements(self, user: User) -> None:
        products = get_all_products(
            products_path=user.products_path, country=self.bazos_country)
        self.advertisements = len(products)

        print("==> Adding advertisements")
        for idx, product in enumerate(products):

            if self.product_already_advertised(product):
                print(
                    f"Skipping[{idx}/{self.advertisements}]: {product.product_path}")
                continue

            print(
                f"Adding[{idx}/{self.advertisements}]: {product.product_path}")

            # product not advertised ADD them
            wait_random_time()
            self.driver.find_element(
                By.CLASS_NAME, 'pridati').click()  # go to add page

            wait_random_time()
            self.driver.find_elements(By.CLASS_NAME, 'iconstblcell')[0].click()
            self.add_advertisement(product=product, user=user)

    def product_already_advertised(self, product: Product) -> bool:
        self.load_page_with_cookies()
        for nadpis in self.driver.find_elements(By.CLASS_NAME, 'nadpis'):
            if product.title in nadpis.text:
                return True
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def bazos_main(cli_args: vars) -> None:
    for country in cli_args['country']:
        print(f"==> Processing country: {country}")
        if cli_args['print_rubrics']:
            bazos_scrapper = BazosScrapper(country=country, cli_args=cli_args)
            bazos_scrapper.check_user_files_available()
            bazos_scrapper.load_page_with_cookies()
            bazos_scrapper.check_authentication()
            bazos_scrapper.print_all_rubrics_and_categories()
            return

        bazos_scrapper = BazosScrapper(country=country, cli_args=cli_args)
        bazos_scrapper.check_user_files_available()
        bazos_scrapper.load_page_with_cookies()
        bazos_scrapper.check_authentication()

        # Restore advertisements
        if '--add-only' not in sys.argv:
            bazos_scrapper.remove_advertisements(user=bazos_scrapper.user)
        bazos_scrapper.add_advertisements(user=bazos_scrapper.user)


if __name__ == '__main__':
    bazos_main({})
