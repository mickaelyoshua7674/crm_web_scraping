from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from typing import List
import time, random
from datetime import datetime

class CRM():
    def __init__(self, chromedriver_path: str) -> None:
        self.CHROMEDRIVER_PATH = chromedriver_path
        self.driver = self.init_driver()

    def init_driver(self):
        # op = webdriver.ChromeOptions()
        # op.add_argument("headless") # don't open a Chrome window
        sc = Service(self.CHROMEDRIVER_PATH)
        return webdriver.Chrome(service=sc)#, options=op)

    def print_current_hour(self) -> None:
        """Print the current hour:min:sec"""
        print(f"Current time {datetime.now()}")

    def random_sleep(self, i: int, f: int) -> None:
        """Randomly choose a float number between i-f and sleep during that random time"""
        time.sleep(random.uniform(i, f))

    def fill_form(self) -> None:
        """Fill UF as PB and show search"""
        # SELECT UF -> PB / SHOW DATA
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.driver.find_element(By.CSS_SELECTOR, ".form.panel"))
        self.random_sleep(1,2)
        self.driver.find_element(By.ID, "uf").click()
        self.random_sleep(1,2)
        Select(self.driver.find_element(By.ID, "uf")).select_by_value("PB")
        print("UF PB selected.")
        self.random_sleep(1,2)
        self.driver.find_element(By.TAG_NAME, "body").click()
        self.random_sleep(1,2)
        self.driver.find_element(By.CSS_SELECTOR, ".w-100.btn-buscar.btnPesquisar").click()
        self.random_sleep(5,7)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        self.random_sleep(1,3)

    def get_last_page(self) -> int:
        return int([p.get_attribute("data-num") for p in self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])

    def get_doctors_data(self) -> List[List[str]]:
        """Get the data from the given div object"""
        divs_med = [d for d in self.driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
                        if "resultado-item resultMedico_" in d.get_attribute("class")] # get all doctor blocks
        self.random_sleep(1,3)
        return [[div.find_element(By.TAG_NAME, "h4").text,
                *[t.text.split(" ")[-1] for t in div.find_elements(By.CSS_SELECTOR, ".col-md-4")],
                div.find_element(By.CSS_SELECTOR, ".col-md").text.split(" ")[-1],
                div.find_element(By.CSS_SELECTOR, ".row.endereco").find_element(By.TAG_NAME, "div").text,
                div.find_element(By.CSS_SELECTOR, ".row.telefone").find_element(By.TAG_NAME, "div").text]
                for div in divs_med]

    def go_to_page(self, page: int) -> None:
        """Go to given page"""
        while True:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            pages_list = [li for li in self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")]
            self.random_sleep(1,2)
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                pages_list[[li.get_attribute("data-num") for li in pages_list].index(str(page))].click()
                break
            except ValueError:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                pages_list[-3].click()
        self.random_sleep(5,7)

    def get_active_page(self) -> int:
        """Collect the current page"""
        self.random_sleep(1,2)
        return int(self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages")\
                        .find_element(By.CSS_SELECTOR, ".paginationjs-page.J-paginationjs-page.active")\
                        .get_attribute("data-num"))