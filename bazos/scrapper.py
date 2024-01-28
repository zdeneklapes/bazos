import os
import pickle  # nosec
import sys
from os import path
from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bazos.core import settings
from bazos.info.product import Product, get_all_products
from bazos.info.rubric_category import get_rubric, get_category
from bazos.shared.utils import parse_yaml, wait_random_time


################################################################################
# BUG: Some images are rotated, when you upload them to bazos

def click_submit_by_value(submits: [WebElement], value: str):
    for submit in submits:
        if submit.get_attribute('value') == value:
            submit.click()


def get_files(credentials_path: path, country: str, phone_number: str) -> tuple:
    cookies_file = credentials_path / f"{settings.COOKIES_FILE}_{country}_{phone_number}.pkl"
    local_storage_file = credentials_path / f"{settings.LOCAL_STORAGE_FILE}_{country}_{phone_number}.pkl"
    return (cookies_file, local_storage_file)


class XPathsBazos:
    select_rubrik = "//div[@class='maincontent']/div[1]/form/select"
    select_category = "//div[@class='maincontent']/form/div[1]/select"
    user_inputs = "//div[@class='maincontent']/form/input"
    delete_pwd_input = "//div[@class='maincontent']/div[2]/form/input[1]"  # nosec
    delete_submit = "//div[@class='maincontent']/div[2]/form/input[4]"

    auth_phone_input = "//div[@class='maincontent']/form[2]/input[2]"
    auth_phone_check_submit = "//div[@class='maincontent']/form/input[4]"
    auth_code_input = "//div[@class='maincontent']/div[1]/form/input[1]"
    auth_code_submit = "//div[@class='maincontent']/div[1]/form/input[3]"

    auth_condition = "//*[@id='podminky']"
    auth_within_pridat_phone_input = "//*[@id='teloverit']"
    auth_within_pridat_button = "/html/body/div/div[3]/div[2]/div/form/input[3]"

    is_auth1 = "//*[@id='teloverit']"
    is_auth2 = "//*[@id='podminky']"

    product_submit = "//div[@class='maincontent']/form/div/input[6]"
    product_rubric = "//div[@class='maincontent']/div[1]/form/select"
    product_category = "//div[@class='maincontent']/form/div[1]/select"
    product_img_input = "//div[@class='maincontent']/form/div[1]/input[3]"


class BazosUrls:
    @staticmethod
    def base_url(country: Literal["cz", "sk"]) -> str:
        return f"https://bazos.{country}"

    @staticmethod
    def moje_inzeraty_url(country: Literal["cz", "sk"]) -> str:
        return path.join(BazosUrls.base_url(country), 'moje-inzeraty.php')

    @staticmethod
    def get_url(country: Literal["cz", "sk"]) -> str:
        return path.join(BazosUrls.base_url(country), 'pridat-inzerat.php')


class BazosDriver:
    def __init__(self, country: str, args: dict):
        self.args = args
        self.country = country
        self.driver = self.get_driver()

    def set_chrome_options(self) -> Options:
        """Sets chrome options for Selenium.
            Chrome options for headless browser is enabled.
            """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_prefs = {}
        # chrome_options.experimental_options["prefs"] = chrome_prefs
        # chrome_prefs["profile.default_content_settings"] = {"images": 2}
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

    def get_driver(self) -> webdriver.Chrome | webdriver.Remote:
        options = self.set_chrome_options()
        if self.args['remote']:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            server = "http://localhost:4444"  # TODO: Add to args or .env
            driver = webdriver.Remote(command_executor=server, options=options)
            return driver
        else:
            webdriver_manager = ChromeDriverManager().install()
            service = Service(executable_path=webdriver_manager)
            driver = webdriver.Chrome(service=service, options=options)
            return driver

    def __del__(self):
        self.driver.quit()


class BazosUser:
    def __init__(self, country: str, args: dict, driver: webdriver.Remote | webdriver.Chrome):
        # super().__init__(country, args)
        self.driver = driver
        self.args = args
        self.country = country
        self.required_keys = ['name', 'phone_number', 'email', 'password', 'psc']
        try:
            yaml_parsed = parse_yaml(filename=path.join(self.args['items_path'], f"user_{country}.yml"))
            for k, v in yaml_parsed.items():
                setattr(self, k, v)

            # Check that all keys are present
            if not all([hasattr(self, k) for k in self.required_keys]):
                raise KeyError(
                    'Some keys are missing, check `user_{country}.yml` file, '
                    'if all keys are present (name, phone_number, email, password, psc)'
                )
        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"Please provide correct `user_{country}.yml` file in `{self.args['items_path']}`")
            sys.exit(1)
        except FileNotFoundError:
            print(f"FileNotFoundError: Please provide `user_{country}.yml` file in `{self.args['items_path']}`")
            sys.exit(1)

    def exists_user_credentials(self, raise_exception: bool = False) -> None:
        cookies_file = self.args["credentials_path"] / f"{settings.COOKIES_FILE}_{self.country}.pkl"
        local_storage_file = self.args["credentials_path"] / f"{settings.LOCAL_STORAGE_FILE}_{self.country}.pkl"
        if not os.path.isfile(cookies_file or not os.path.isfile(local_storage_file)):  # nosec
            if raise_exception:
                raise FileNotFoundError("User files not found, please login - login flag: --login")

    def is_authenticated(self) -> bool:
        user_input = self.driver.find_elements(By.XPATH, XPathsBazos.user_inputs)
        if len(user_input) != 3:  # Mean is Authenticated, because there is not "Overit" button
            return False

    def authenticate(self) -> None:
        self.driver.get(BazosUrls.moje_inzeraty_url(self.country))

        # Prepare authentication
        telefon_input = self.driver.find_element(By.XPATH, XPathsBazos.auth_phone_input)
        telefon_input.clear()
        phone_number = getattr(self, 'phone_number')
        telefon_input.send_keys(phone_number)
        self.driver.find_element(By.XPATH, XPathsBazos.auth_phone_check_submit).click()  # Submit

        # Authenticate
        code_input = self.driver.find_element(By.XPATH, XPathsBazos.auth_code_input)
        code_input.clear()
        code_input.send_keys(input('Please provide authentification code sended to your phone: '))
        self.driver.find_element(By.XPATH, XPathsBazos.auth_code_submit).click()  # Submit

    def save_user_credentials(self) -> None:
        cookies_file, local_storage_file = get_files(
            credentials_path=self.args["credentials_path"],
            country=self.country,
            phone_number=getattr(self, 'phone_number')
        )
        cookies = self.driver.get_cookies()
        local_storage = self.driver.execute_script("return window.localStorage;")
        pickle.dump(cookies, file=open(cookies_file.__str__(), "wb"))  # nosec
        pickle.dump(local_storage, file=open(local_storage_file, "wb"))  # nosec


class BazosScrapper:
    def __init__(self, country: str, args: dict, user: BazosUser, driver: webdriver.Remote | webdriver.Chrome):
        # super().__init__(country, args)
        self.driver = driver
        self.args = args
        self.country = country
        self.user = user
        self.advertisements: int

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

    def load_page_with_cookies(self, page: Literal["my_adds", "create"] = "my_adds") -> None:
        cookies_file, _ = get_files(credentials_path=self.args["credentials_path"],
                                    country=self.country,
                                    phone_number=getattr(self.user, 'phone_number'))
        if page == "my_adds":
            self.driver.get(BazosUrls.moje_inzeraty_url(self.country))
        elif page == "create":
            self.driver.get(BazosUrls.get_url(self.country))

        for cookie_dict in pickle.load(open(cookies_file, 'rb')):  # nosec
            self.driver.add_cookie(cookie_dict)

        if page == "my_adds":
            self.driver.get(BazosUrls.moje_inzeraty_url(self.country))
        elif page == "create":
            self.driver.get(BazosUrls.get_url(self.country))

    def delete_advertisement(self):
        del_btn = self.driver.find_element(By.CLASS_NAME, 'inzeratydetdel').find_element(By.TAG_NAME, 'a')
        del_btn.click()
        pwd_input = self.driver.find_element(By.XPATH, XPathsBazos.delete_pwd_input)
        pwd_input.clear()
        pwd_input.send_keys(getattr(self.user, 'password'))
        if self.args['mode'] == 'slow':
            wait_random_time(coef=1)
        self.driver.find_element(By.XPATH, XPathsBazos.delete_submit).click()  # Submit-Delete

    def delete_all_advertisements(self):
        self.advertisements = len(self.driver.find_elements(By.CLASS_NAME, 'nadpis'))

        if self.args['verbose']:
            print("==> Removing old advertisements")
        for i in range(self.advertisements):
            if self.args['mode'] == 'slow':
                wait_random_time(coef=1)
            element = self.driver.find_element(By.CLASS_NAME, 'nadpis')
            if self.args['verbose']:
                print(f"Removing[{i}/{self.advertisements}]: {element.text}")

            #
            element.find_element(By.TAG_NAME, 'a').click()
            self.delete_advertisement()

    def create_advertisement(self, product: Product):
        # Rubrik
        select_rubrik = Select(self.driver.find_element(By.XPATH, XPathsBazos.product_rubric))
        select_rubrik.select_by_visible_text(get_rubric(self.country, product.rubric))

        # Product
        select_category = Select(self.driver.find_element(By.XPATH, XPathsBazos.product_category))
        select_category.select_by_visible_text(get_category(self.country, product.rubric, product.category))
        self.driver.find_element(By.ID, 'nadpis').send_keys(product.title)
        self.driver.find_element(By.ID, 'popis').send_keys(product.description)
        self.driver.find_element(By.ID, 'cena').send_keys(product.get_location_price(self.country))

        self.driver.find_element(By.ID, 'lokalita').clear()
        self.driver.find_element(By.ID, 'lokalita').send_keys(getattr(self.user, 'psc'))
        self.driver.find_element(By.ID, 'jmeno').clear()
        self.driver.find_element(By.ID, 'jmeno').send_keys(getattr(self.user, 'name'))
        self.driver.find_element(By.ID, 'telefoni').clear()
        self.driver.find_element(By.ID, 'telefoni').send_keys(getattr(self.user, 'phone_number'))
        self.driver.find_element(By.ID, 'maili').clear()
        self.driver.find_element(By.ID, 'maili').send_keys(getattr(self.user, 'email'))
        self.driver.find_element(By.ID, 'heslobazar').clear()
        self.driver.find_element(By.ID, 'heslobazar').send_keys(getattr(self.user, 'password'))

        self.driver.find_element(By.CLASS_NAME, 'ovse').click()
        self.driver.find_element(By.XPATH, XPathsBazos.product_img_input).send_keys('\n'.join(product.images))

        if self.args['mode'] == 'slow':
            wait_random_time(coef=1)
        self.driver.find_element(By.XPATH, XPathsBazos.product_submit).click()

    def create_all_advertisements(self) -> None:
        products = get_all_products(products_path=self.args["items_path"], country=self.country)
        self.advertisements = len(products)

        if self.args['verbose']:
            print("==> Adding advertisements")
        for idx, product in enumerate(products):
            if self.args['mode'] == 'slow':
                wait_random_time(coef=1)

            if self.product_already_advertised(product):
                if self.args['verbose']:
                    print(f"Skipping[{idx}/{self.advertisements}]: {product.product_path}")
                continue

            if self.args['verbose']:
                print(f"Adding[{idx}/{self.advertisements}]: {product.product_path}")

            # product not advertised ADD them
            self.driver.find_element(By.CLASS_NAME, 'pridati').click()  # go to add page

            self.driver.find_elements(By.CLASS_NAME, 'iconstblcell')[0].click()
            # self.load_page_with_cookies(page="create")

            # TODO: Fix authentification
            if self.user.is_authenticated():
                self.user.authenticate()
                # self.driver.find_element(By.XPATH, XPathsBazos.auth_condition).click()
                # self.driver.find_element(By.XPATH, XPathsBazos.auth_within_pridat_phone_input).clear()
                # self.driver.find_element(
                # By.XPATH, XPathsBazos.auth_within_pridat_phone_input
                # ).send_keys(getattr(self.user, 'phone_number'))
                # self.driver.find_element(By.XPATH, XPathsBazos.auth_within_pridat_button).click()
                # self.driver.find_element(By.XPATH, XPathsBazos.auth_code_input).clear()
                # (self.driver.find_element(By.XPATH, XPathsBazos.auth_code_input)
                #  .send_keys(input('Please provide authentification code sended to your phone: ')))
                # self.driver.find_element(By.XPATH, XPathsBazos.auth_code_submit).click()

            self.create_advertisement(product=product)

    def product_already_advertised(self, product: Product) -> bool:
        self.load_page_with_cookies()
        for nadpis in self.driver.find_elements(By.CLASS_NAME, 'nadpis'):
            if product.title in nadpis.text:
                return True
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
