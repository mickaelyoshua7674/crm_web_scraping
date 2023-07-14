from helper import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from os.path import exists
from threading import Thread

CHROMEDRIVER_PATH = "chromedriver.exe"
COLUMNS = ["crm", "name", "data_inscricao", "prim_inscricao", "inscricao", "situacao", "endereco", "telefone"]

if not exists("crm_pb_data.csv"):
    pd.DataFrame(columns=COLUMNS).to_csv("crm_pb_data.csv", header=True, index=False)

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
driver_even = driver_odd = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)

def main(pages_type: str, driver):
    # SELECT UF -> PB / SHOW DATA
    assert pages_type == "even" or pages_type == "odd", "'pages_type' must be 'even' or 'odd'"
    # op = webdriver.ChromeOptions()
    # op.add_argument("headless") # don't open a Chrome window
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)
    driver.get("https://crmpb.org.br/busca-medicos/")
    random_sleep(3,5)
    fill_form(driver)
    last_page = int([p.get_attribute("data-num") for p in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])
    if pages_type=="even":
        pages = [p for p in range(1, last_page+1) if p%2==0]
    else:
        pages = [p for p in range(1, last_page+1) if p%2==1]
    for p in pages:
        if p == 1:
            # GET FIRST PAGE DATA AND SAVE
            print_current_hour()
            print("Getting data...")
            divs_med = [d for d in driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
                        if "resultado-item resultMedico_" in d.get_attribute("class")]
            random_sleep(1,3)
            data = [get_doctor_data(div) for div in divs_med]
            print("Data collected.\n")
            pd.DataFrame(data=data, columns=COLUMNS).to_csv("crm_pb_data.csv", header=False, index=False, mode="a")
        else:
            print_current_hour()
            random_sleep(5,7)
            [li for li in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")
            if li.get_attribute("data-num") == str(p)][0].click()
            print(f"Page {p}")
            random_sleep(7,9)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
            
            print("Getting data...")
            divs_med = [d for d in driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
                        if "resultado-item resultMedico_" in d.get_attribute("class")]
            random_sleep(1,3)
            data = [get_doctor_data(div) for div in divs_med]
            print("Data collected.\n")
            pd.DataFrame(data=data, columns=COLUMNS).to_csv("crm_pb_data.csv", header=False, index=False, mode="a")

            random_sleep(1,3)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            random_sleep(1,3)
    driver.quit()

Thread(target=main("odd", driver_odd)).start()
Thread(target=main("even", driver_even)).start()