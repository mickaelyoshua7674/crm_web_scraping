from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from typing import List, Union
import time, random, traceback
import pandas as pd

class CRM():
    def __init__(self, chromedriver_path: str) -> None:
        self.CHROMEDRIVER_PATH = chromedriver_path
        self.driver = self.init_driver()

    def init_driver(self):
        op = webdriver.ChromeOptions()
        op.add_argument("log-level=3") # https://stackoverflow.com/questions/46744968/how-to-suppress-console-error-warning-info-messages-when-executing-selenium-pyth
        # op.add_argument("headless") # don't open a Chrome window
        sc = Service(self.CHROMEDRIVER_PATH)
        return webdriver.Chrome(service=sc, options=op)

    def random_sleep(self, i: Union[int, float], f: Union[int, float]) -> None:
        """Randomly choose a float number between i-f and sleep during that random time"""
        time.sleep(random.uniform(i, f))

    def get_values_from_field_form(self, id: str) -> List[str]:
        """Get all available values in form's field"""
        elem = self.driver.find_element(By.ID, id)
        self.random_sleep(1,2)
        return [e.text for e in elem.find_elements(By.TAG_NAME, "option")]

    def __fill_field(self, id: str, value: str) -> None:
        """
        Find the field element and click it
        Select the desired value
        Click on 'body'
        """
        self.driver.find_element(By.ID, id).click()
        self.random_sleep(1,2)
        Select(self.driver.find_element(By.ID, id)).select_by_visible_text(value)
        print(f"{value} selected.\n")
        self.random_sleep(1,2)
        self.driver.find_element(By.TAG_NAME, "body").click()
        self.random_sleep(1,2)

    def fill_form(self, uf: str, mun: str="Todos", espec: str="Todas") -> None:
        """Fill UF as PB and show search"""
        # SELECT UF -> PB / SHOW DATA
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.driver.find_element(By.CSS_SELECTOR, ".form.panel"))
        self.random_sleep(1,2)

        self.__fill_field("uf", uf)
        self.__fill_field("municipio", mun)
        self.__fill_field("especialidade", espec)

        self.driver.find_element(By.CSS_SELECTOR, ".w-100.btn-buscar.btnPesquisar").click()
        self.random_sleep(5,7)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        self.random_sleep(1,3)

    def get_last_page(self) -> int:
        return int([p.get_attribute("data-num") for p in self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])

    def get_doctors_data(self) -> List[List[str]]:
        """Get the data from the given div object"""
        # divs_med = [d for d in self.driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.CLASS_NAME, "resultado-item")] # get all doctor blocks
        texts = [div.text.splitlines() for div in self.driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.CLASS_NAME, "resultado-item")]
        return [[text[0],
                 text[1].split(": ")[-1],
                 text[2].split(": ")[-1],
                 text[3].split(": ")[-1],
                 text[4].split(": ")[-1],
                 text[5].split(": ")[-1],
                 " / ".join(text[text.index('Especialidades/Áreas de Atuação:')+1:-2]),
                 text[-2].split(": ")[-1],
                 text[-1].split(": ")[-1]] for text in texts]
    
    def go_to_page(self, page: int) -> None:
        """Go to given page"""
        while True:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            self.random_sleep(.1,1)
            pages_list = [li for li in self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")]
            self.random_sleep(.1,1)
            
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                pages_list[[li.get_attribute("data-num") for li in pages_list].index(str(page))].click()
                print(f"Next page to collect: {self.get_active_page()}")
                break
            except ValueError:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                pages_list[-3].click()

            print(f"Page: {self.get_active_page()}")
            self.random_sleep(2,4)

    def get_active_page(self) -> int:
        """Collect the current page"""
        self.random_sleep(1,2)
        return int(self.driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages")\
                        .find_element(By.CSS_SELECTOR, ".paginationjs-page.J-paginationjs-page.active")\
                        .get_attribute("data-num"))
    
    def concat_data(self, file_name: str, columns: List[str]) -> None:
        print("Getting data...")
        self.random_sleep(1,2)
        data = self.get_doctors_data()
        print("Data collected.\n")

        collected_crm = pd.read_csv(file_name)["crm"].unique()
        for line in [d for d in data]:
            crm = line[1]
            if crm in collected_crm:
                data.remove(line)
                print(f"{crm} already collected.\n")
                
        pd.DataFrame(data=data, columns=columns).to_csv(file_name, header=False, index=False, mode="a")

    def get_result_text(self) -> str:
        if self.driver.find_element(By.CSS_SELECTOR, ".resultado-item").text != "Nenhum resultado encontrado":
            return True
        return False