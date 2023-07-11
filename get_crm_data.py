from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import random

CHROMEDRIVER_PATH = "chromedriver.exe"

def random_sleep(i: int, f: int) -> None:
    """Randomly choose a float number between i-f and sleep during that random time"""
    time.sleep(random.uniform(i, f))

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)

# SELECT UF -> PB / SHOW DATA
driver.get("https://crmpb.org.br/busca-medicos/")
random_sleep(3,5)
driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, ".form.panel"))
random_sleep(1,3)
driver.find_element(By.ID, "uf").click()
random_sleep(1,3)
Select(driver.find_element(By.ID, "uf")).select_by_value("PB")
print("UF PB selected.")
random_sleep(1,3)
driver.find_element(By.TAG_NAME, "body").click()
random_sleep(1,3)
driver.find_element(By.CSS_SELECTOR, ".w-100.btn-buscar.btnPesquisar").click()
random_sleep(5,7)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
random_sleep(1,3)

last_page = int([p.get_attribute("data-num") for p in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])
print(last_page)
random_sleep(1,3)
for p in range(1, last_page+1):
    pages_list = driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")
    random_sleep(1,3)
    for obj in pages_list:
        if obj.get_attribute("data-num") == str(p):
            obj.click()
            print(f"In page {p}")
            random_sleep(5,7)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
            random_sleep(1,3)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            random_sleep(1,3)




driver.quit()
